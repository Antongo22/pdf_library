import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

from app.routers import pdfs

app = FastAPI(title="PDF Library", description="Online PDF reader application")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(pdfs.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

if __name__ == "__main__":
    # Запускаем с настройками для HTTPS
    # Сертификаты должны быть настроены на уровне сервера
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
