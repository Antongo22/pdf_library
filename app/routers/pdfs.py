import os
from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from pathlib import Path
from typing import List, Optional
import logging

router = APIRouter(
    prefix="/pdf",
    tags=["documents"]
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


def get_pdf_files(directory: str) -> list[dict]:
    """
    Получает список PDF и Markdown файлов в указанной директории
    """
    files = []
    base_dir = str(get_pdf_dir())  # Преобразуем Path в строку
    
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and (file.lower().endswith('.pdf') or file.lower().endswith('.md')):
            # Определяем тип файла для иконки
            file_type = 'pdf' if file.lower().endswith('.pdf') else 'markdown'
            # Используем полный путь для корректного URL-кодирования
            rel_path = os.path.relpath(file_path, base_dir).replace('\\', '/')
            files.append({
                'name': file,
                'path': rel_path,
                'encoded_path': rel_path,  # Добавляем полный путь для URL
                'type': file_type
            })
    return sorted(files, key=lambda x: x['name'].lower())


def get_directories(directory: str) -> list[dict]:
    """
    Получает список подпапок в указанной директории
    """
    directories = []
    base_dir = get_pdf_dir()  # Получаем базовую директорию
    
    for dir_path in Path(directory).iterdir():
        if dir_path.is_dir():
            # Используем str() для обоих путей перед relative_to
            rel_path = os.path.relpath(str(dir_path), str(base_dir)).replace("\\", "/")
            directories.append({
                "name": dir_path.name,
                "path": f"/pdf/?folder={rel_path}",
                "icon": "fas fa-folder"
            })
    return sorted(directories, key=lambda x: x["name"])


def generate_breadcrumbs(folder: str) -> List[dict]:
    """
    Генерирует хлебные крошки для навигации
    """
    breadcrumbs = [{"name": "Главная", "path": "/pdf/"}]
    
    if not folder or folder == "":
        return breadcrumbs
        
    parts = Path(folder).parts
    current_path = ""
    
    for part in parts:
        current_path = str(Path(current_path) / part)
        breadcrumbs.append({
            "name": part,
            "path": f"/pdf/?folder={current_path}"
        })
        
    return breadcrumbs


@router.get("/", response_class=HTMLResponse)
async def list_pdfs(request: Request, folder: str = ""):
    """
    Выводит список PDF и Markdown файлов и подпапок в директории
    """
    try:
        base_dir = str(get_pdf_dir())  # Преобразуем Path в строку
        current_dir = os.path.normpath(os.path.join(base_dir, folder))
        
        # Проверка на выход за пределы корневой директории
        if not current_dir.startswith(base_dir):
            raise HTTPException(status_code=403, detail="Access denied")
            
        if not os.path.exists(current_dir) or not os.path.isdir(current_dir):
            raise HTTPException(status_code=404, detail="Directory not found")
        
        # Получаем списки директорий и файлов
        directories = get_directories(current_dir)
        files = get_pdf_files(current_dir)
        
        # Генерируем хлебные крошки
        breadcrumbs = generate_breadcrumbs(folder)
        
        return templates.TemplateResponse(
            "pdf_list.html",
            {
                "request": request,
                "files": files,
                "directories": directories,
                "breadcrumbs": breadcrumbs,
                "current_folder": folder
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error listing files: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/view/{file_path:path}")
async def view_pdf(request: Request, file_path: str):
    """View a PDF or Markdown file"""
    try:
        # Разбиваем путь на директорию и имя файла
        file_parts = Path(file_path)
        file_name = file_parts.name
        folder = str(file_parts.parent) if str(file_parts.parent) != "." else None
        
        # Получаем полный путь к файлу
        base_dir = get_subfolder_path(folder)
        file_path_full = base_dir / file_name
        
        if not file_path_full.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Формируем URL для загрузки
        download_url = f"/pdf/download/{file_path}"
        back_url = f"/pdf/?folder={folder}" if folder else "/pdf/"
        
        # В зависимости от типа файла выбираем шаблон
        if file_name.lower().endswith('.md'):
            # Читаем содержимое Markdown файла
            try:
                # Пробуем разные кодировки для чтения файла
                encodings = ['utf-8', 'cp1251', 'latin-1']
                content = None
                
                for encoding in encodings:
                    try:
                        with open(file_path_full, 'r', encoding=encoding) as file:
                            content = file.read()
                        break  # Если успешно прочитали, выходим из цикла
                    except UnicodeDecodeError:
                        continue
                
                if content is None:
                    raise ValueError(f"Не удалось прочитать файл ни с одной из кодировок: {encodings}")
                
                # Импортируем markdown при необходимости
                try:
                    import markdown
                    from markdown.extensions import codehilite, fenced_code, tables
                    
                    # Конфигурируем расширения без проблемных параметров
                    # Используем только префикс языка, остальные параметры не применяем
                    fenced_code_ext = fenced_code.FencedCodeExtension(lang_prefix='language-')
                    tables_ext = tables.TableExtension()
                    
                    # Преобразуем Markdown в HTML с сохранением информации о языке программирования
                    # Заменяем форматирование блоков кода для лучшей интеграции с highlight.js
                    html_content = markdown.markdown(
                        content, 
                        extensions=[fenced_code_ext, tables_ext, 'toc', 'nl2br']
                    )
                    
                    # Дополнительная обработка для Dockerfile и других специальных языков
                    import re
                    # Заменить dockerfile на language-dockerfile для корректной подсветки
                    html_content = re.sub(r'<code class=[\'"]dockerfile[\'"]>', '<code class="language-dockerfile">', html_content)
                except ImportError:
                    # Если модуль не установлен, используем простой текстовый вывод
                    html_content = f"<pre>{content}</pre>"
                
                return templates.TemplateResponse(
                    "markdown_viewer.html", 
                    {
                        "request": request, 
                        "title": file_path_full.stem.replace("_", " ").title(), 
                        "content": html_content,
                        "back_url": back_url,
                        "file_path": file_path  # Добавляем путь к файлу для скачивания
                    }
                )
            except Exception as e:
                logging.error(f"Error reading markdown file: {str(e)}")
                raise HTTPException(status_code=500, detail="Error reading markdown file")
        elif file_name.lower().endswith('.pdf'):
            # Отображение PDF-файла
            return templates.TemplateResponse(
                "pdf_viewer.html", 
                {
                    "request": request, 
                    "pdf_name": file_path_full.stem.replace("_", " ").title(), 
                    "pdf_url": download_url,
                    "back_url": back_url
                }
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error viewing file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/download/{file_path:path}")
async def download_file(file_path: str):
    """Download a document file (PDF or Markdown)"""
    try:
        # Разбиваем путь на директорию и имя файла
        file_parts = Path(file_path)
        file_name = file_parts.name
        folder = str(file_parts.parent) if str(file_parts.parent) != "." else None
        
        # Получаем полный путь к файлу
        file_dir = get_subfolder_path(folder)
        file_path_full = file_dir / file_name
        
        if not file_path_full.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Определяем media_type на основе расширения файла
        if file_name.lower().endswith('.pdf'):
            media_type = "application/pdf"
        elif file_name.lower().endswith('.md'):
            media_type = "text/markdown"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        return FileResponse(
            path=str(file_path_full), 
            media_type=media_type, 
            filename=file_name
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error downloading file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



