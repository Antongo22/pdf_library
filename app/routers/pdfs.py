import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path

router = APIRouter(
    prefix="/pdf",
    tags=["PDF Files"],
)

# Templates
templates = Jinja2Templates(directory="app/templates")

# Path to PDF files - проверяем несколько путей для совместимости
def get_pdf_dir():
    paths_to_check = [
        Path("app/pdfs"),
        Path("pdf_uploads"),
        Path("./app/pdfs"),
        Path("./pdf_uploads")
    ]
    
    # Проверяем, какая директория существует и содержит файлы
    for path in paths_to_check:
        if path.exists() and any(path.glob("*.pdf")):
            return path
    
    # Если ни в одной директории нет PDF файлов, используем app/pdfs, создав его при необходимости
    default_path = Path("app/pdfs")
    default_path.mkdir(parents=True, exist_ok=True)
    return default_path

@router.get("/", response_class=HTMLResponse)
async def list_pdfs(request: Request):
    """List all available PDF files"""
    pdf_files = []
    
    # Получаем директорию с PDF файлами
    pdf_dir = get_pdf_dir()
    
    # Список всех PDF файлов
    for file in pdf_dir.glob("*.pdf"):
        pdf_files.append({
            "name": file.stem.replace("_", " ").title(),
            "filename": file.name,
            "path": f"/pdf/view/{file.name}",
            "download": f"/pdf/download/{file.name}",
            "size": round(file.stat().st_size / (1024 * 1024), 2)  # Size in MB
        })
    
    return templates.TemplateResponse(
        "pdf_list.html", 
        {"request": request, "pdf_files": pdf_files}
    )

@router.get("/view/{filename}")
async def view_pdf(request: Request, filename: str):
    """View a PDF file"""
    # Получаем директорию с PDF файлами
    pdf_dir = get_pdf_dir()
    pdf_path = pdf_dir / filename
    
    if not pdf_path.exists() or not filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    return templates.TemplateResponse(
        "pdf_viewer.html", 
        {"request": request, "pdf_name": pdf_path.stem.replace("_", " ").title(), "pdf_url": f"/pdf/download/{filename}"}
    )

@router.get("/download/{filename}")
async def download_pdf(filename: str):
    """Download a PDF file"""
    # Получаем директорию с PDF файлами
    pdf_dir = get_pdf_dir()
    pdf_path = pdf_dir / filename
    
    if not pdf_path.exists() or not filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    return FileResponse(pdf_path, media_type="application/pdf", filename=filename)
