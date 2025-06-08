import os
from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from typing import List, Optional

router = APIRouter(
    prefix="/pdf",
    tags=["PDF Files"],
)

# Templates
templates = Jinja2Templates(directory="app/templates")

# Path to PDF files - проверяем несколько путей для совместимости
def get_pdf_dir():
    """Возвращает базовую директорию для PDF-файлов"""
    # Используем только директорию pdf_uploads и преобразуем в абсолютный путь
    base_dir = Path.cwd()
    
    # Проверяем несколько вариантов расположения
    possible_paths = [
        base_dir / "pdf_uploads",
        base_dir / "app" / "pdfs",
        Path("pdf_uploads").resolve(),
        Path("app/pdfs").resolve()
    ]
    
    # Проверяем, что директория существует
    for path in possible_paths:
        if path.exists() and path.is_dir():
            return path.resolve()  # Возвращаем абсолютный путь
    
    # Если директория не найдена, используем путь по умолчанию
    default_path = base_dir / "pdf_uploads"
    default_path.mkdir(parents=True, exist_ok=True)
    return default_path.resolve()  # Возвращаем абсолютный путь


def get_subfolder_path(subfolder: Optional[str] = None) -> Path:
    """Получает путь к подпапке относительно базовой директории PDF"""
    base_dir = get_pdf_dir()
    
    # Если подпапка не указана, возвращаем базовую директорию
    if not subfolder or subfolder == "" or subfolder == "/":
        return base_dir
        
    # Нормализуем путь и проверяем, что он не выходит за пределы базовой директории
    subfolder_path = (base_dir / subfolder).resolve()
    if not str(subfolder_path).startswith(str(base_dir.resolve())):
        raise HTTPException(status_code=403, detail="Access denied")
        
    # Проверяем, что директория существует
    if not subfolder_path.exists():
        raise HTTPException(status_code=404, detail="Folder not found")
        
    return subfolder_path


def create_breadcrumbs(subfolder: Optional[str] = None) -> List[dict]:
    """Создает список хлебных крошек для навигации"""
    breadcrumbs = [{"name": "Главная", "path": "/pdf/"}]
    
    if not subfolder or subfolder == "":
        return breadcrumbs
        
    parts = Path(subfolder).parts
    current_path = ""
    
    for part in parts:
        current_path = str(Path(current_path) / part)
        breadcrumbs.append({
            "name": part,
            "path": f"/pdf/?folder={current_path}"
        })
        
    return breadcrumbs

@router.get("/", response_class=HTMLResponse)
async def list_pdfs(
    request: Request, 
    folder: Optional[str] = Query(None, description="Путь к папке для просмотра")
):
    """Показывает все доступные PDF-файлы и директории в указанной папке"""
    # Получаем путь к текущей директории
    current_dir = get_subfolder_path(folder)
    
    # Создаем хлебные крошки для навигации
    breadcrumbs = create_breadcrumbs(folder)
    
    # Список директорий
    directories = []
    for dir_path in current_dir.iterdir():
        if dir_path.is_dir():
            rel_path = str(dir_path.relative_to(get_pdf_dir())).replace("\\", "/")
            directories.append({
                "name": dir_path.name,
                "path": f"/pdf/?folder={rel_path}",
                "icon": "fas fa-folder"
            })
    
    # Список PDF-файлов
    pdf_files = []
    for file in current_dir.glob("*.pdf"):
        # Относительный путь для формирования URL
        rel_path = str(file.parent.relative_to(get_pdf_dir())).replace("\\", "/") if folder else ""
        file_url_path = f"{rel_path}/{file.name}" if rel_path else file.name
        
        pdf_files.append({
            "name": file.stem.replace("_", " ").title(),
            "filename": file.name,
            "path": f"/pdf/view/{file_url_path}",
            "download": f"/pdf/download/{file_url_path}",
            "size": round(file.stat().st_size / (1024 * 1024), 2),  # Size in MB
            "icon": "far fa-file-pdf",
            "is_file": True
        })
    
    # Сортируем сначала директории, потом файлы
    all_items = sorted(directories, key=lambda x: x["name"]) + sorted(pdf_files, key=lambda x: x["name"])
    
    return templates.TemplateResponse(
        "pdf_list.html", 
        {
            "request": request, 
            "items": all_items,
            "breadcrumbs": breadcrumbs,
            "current_folder": folder or ""
        }
    )

@router.get("/view/{file_path:path}")
async def view_pdf(request: Request, file_path: str):
    """View a PDF file"""
    # Разбиваем путь на директорию и имя файла
    file_parts = Path(file_path)
    file_name = file_parts.name
    folder = str(file_parts.parent) if str(file_parts.parent) != "." else None
    
    # Получаем полный путь к файлу
    pdf_dir = get_subfolder_path(folder)
    pdf_path = pdf_dir / file_name
    
    if not pdf_path.exists() or not file_name.lower().endswith('.pdf'):
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    # Формируем URL для загрузки
    download_url = f"/pdf/download/{file_path}"
    
    return templates.TemplateResponse(
        "pdf_viewer.html", 
        {
            "request": request, 
            "pdf_name": pdf_path.stem.replace("_", " ").title(), 
            "pdf_url": download_url,
            "back_url": f"/pdf/?folder={folder}" if folder else "/pdf/"
        }
    )

@router.get("/download/{file_path:path}")
async def download_pdf(file_path: str):
    """Download a PDF file"""
    # Разбиваем путь на директорию и имя файла
    file_parts = Path(file_path)
    file_name = file_parts.name
    folder = str(file_parts.parent) if str(file_parts.parent) != "." else None
    
    # Получаем полный путь к файлу
    pdf_dir = get_subfolder_path(folder)
    pdf_path = pdf_dir / file_name
    
    if not pdf_path.exists() or not file_name.lower().endswith('.pdf'):
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    return FileResponse(pdf_path, media_type="application/pdf", filename=file_name)



