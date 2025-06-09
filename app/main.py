import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from pathlib import Path

from app.routers import pdfs

is_docker = os.environ.get('RUNNING_IN_DOCKER', 'false').lower() == 'true'

if is_docker:
    app = FastAPI(
        title="Knowledge Library",
        description="Библиотека знаний - Просмотр документов в разных форматах",
        docs_url=None,
        redoc_url=None
    )
else:
    app = FastAPI(
        title="Knowledge Library",
        description="Библиотека знаний - Просмотр документов в разных форматах"
    )

app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")

templates = Jinja2Templates(directory="app/templates")

# Обработчики ошибок
@app.exception_handler(404)
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404
        )
    return templates.TemplateResponse(
        "404.html",
        {"request": request, "detail": str(exc.detail)},
        status_code=exc.status_code
    )

app.include_router(pdfs.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "has_markdown": True})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
