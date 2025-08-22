import os
import markdown
from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, Response
from pathlib import Path
from typing import List, Optional

router = APIRouter(
    prefix="/markdown",
    tags=["markdown"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="app/templates")

# Используем ту же директорию, что и для PDF-файлов
def get_markdown_dir():
    """Возвращает базовую директорию для Markdown-файлов"""
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
    """Получаем безопасный путь к подпапке, предотвращаем выход за пределы базовой директории"""
    base_dir = get_markdown_dir()
    
    if not subfolder:
        return base_dir
    
    # Преобразуем путь к подпапке в объект Path и убедимся, что он находится внутри базовой директории
    try:
        # Нормализуем путь и удалим символы, которые могут быть использованы для выхода из директории
        subfolder_path = (base_dir / subfolder).resolve()
        
        # Проверяем, что путь находится внутри базовой директории
        if not str(subfolder_path).startswith(str(base_dir)):
            raise HTTPException(status_code=400, detail="Invalid folder path")
        
        if not subfolder_path.exists():
            raise HTTPException(status_code=404, detail="Folder not found")
        
        return subfolder_path
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=400, detail="Invalid folder path")


def create_breadcrumbs(folder: Optional[str] = None):
    """Создаёт иерархию директорий для хлебных крошек"""
    breadcrumbs = [{"name": "Главная", "path": "/"}]
    
    if not folder:
        return breadcrumbs
    
    parts = folder.split('/')
    current_path = ""
    
    for part in parts:
        if not part:  # Пропускаем пустые части
            continue
            
        current_path = f"{current_path}/{part}" if current_path else part
        breadcrumbs.append({"name": part, "path": f"/markdown/?folder={current_path}"})
    
    return breadcrumbs


@router.get("/", response_class=HTMLResponse)
async def list_markdown_files(
    request: Request, 
    folder: Optional[str] = Query(None, description="Путь к папке для просмотра")
):
    """Отображает список Markdown файлов в директории"""
    current_dir = get_subfolder_path(folder)
    breadcrumbs = create_breadcrumbs(folder)
    
    directories = []
    markdown_files = []
    
    # Получаем содержимое директории
    for file_path in current_dir.iterdir():
        if file_path.is_dir():
            rel_path = str(file_path.relative_to(get_markdown_dir())).replace("\\", "/")
            directories.append({
                "name": file_path.name,
                "path": rel_path
            })
        elif file_path.suffix.lower() in ['.md', '.markdown']:
            rel_path = str(file_path.relative_to(get_markdown_dir())).replace("\\", "/")
            markdown_files.append({
                "name": file_path.name,
                "path": rel_path
            })
    
    # Сортируем директории и файлы по имени
    directories.sort(key=lambda x: x["name"].lower())
    markdown_files.sort(key=lambda x: x["name"].lower())
    
    # Передаем данные в шаблон
    return templates.TemplateResponse(
        "markdown_list.html", 
        {
            "request": request, 
            "markdown_files": markdown_files,
            "directories": directories,
            "current_folder": folder or "",
            "breadcrumbs": breadcrumbs
        }
    )


@router.get("/view/{file_path:path}", response_class=HTMLResponse)
async def view_markdown(request: Request, file_path: str):
    """Просмотр Markdown файлов"""
    print(f"MARKDOWN DEBUG: Accessing file_path = {file_path}")
    
    try:
        # Базовая директория для PDF файлов
        base_dir = Path("pdf_uploads")
        full_path = base_dir / file_path
        
        print(f"MARKDOWN DEBUG: full_path = {full_path}")
        print(f"MARKDOWN DEBUG: full_path.parent = {full_path.parent}")
        
        # Проверяем, что файл существует и имеет расширение .md
        if not full_path.exists() or not full_path.suffix.lower() == '.md':
            raise HTTPException(status_code=404, detail="Markdown файл не найден")
        
        # Читаем содержимое файла
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Преобразуем Markdown в HTML
        html_content = markdown.markdown(
            content, 
            extensions=['extra', 'codehilite', 'tables']
        )
        
        # Получаем относительный путь к директории для кнопки "Назад"
        parent_folder = str(full_path.parent.relative_to(base_dir)).replace("\\", "/")
        print(f"MARKDOWN DEBUG: parent_folder = '{parent_folder}'")
        
        # Формируем URL для кнопки "Назад"
        back_url = f"/pdf/?folder={parent_folder}" if parent_folder and parent_folder != "." else "/pdf/"
        print(f"MARKDOWN DEBUG: back_url = '{back_url}'")
        
        return templates.TemplateResponse(
            "markdown_viewer.html", 
            {
                "request": request, 
                "content": html_content,
                "title": full_path.name,
                "file_path": file_path,
                "back_url": back_url
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error viewing Markdown file: {str(e)}")


@router.get("/download/{file_path:path}")
async def download_markdown(file_path: str):
    """Скачивание Markdown файла"""
    base_dir = get_markdown_dir()
    
    try:
        # Преобразуем путь к файлу в объект Path и убедимся, что он находится внутри базовой директории
        full_path = (base_dir / file_path).resolve()
        
        # Проверяем, что файл существует и находится внутри базовой директории
        if not full_path.exists() or not str(full_path).startswith(str(base_dir)):
            raise HTTPException(status_code=404, detail="File not found")
        
        file_name = full_path.name
        return FileResponse(full_path, filename=file_name)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")
