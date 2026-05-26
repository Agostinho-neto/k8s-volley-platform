# app/main.py

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes.players import router as players_router
from app.logging_config import configure_logging
from app.middleware import RequestLoggingMiddleware


configure_logging()
app = FastAPI(
    title="Volley Club Platform",
    version="1.0.0",
)

app.add_middleware(RequestLoggingMiddleware)

app.include_router(players_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return FileResponse("app/static/index.html")
