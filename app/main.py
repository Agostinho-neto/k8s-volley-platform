# app/main.py

from fastapi import FastAPI
from app.routes.players import router as players_router

app = FastAPI(
    title="Volley Club Platform",
    version="1.0.0"
)

app.include_router(players_router)

@app.get("/")
def root():
    return {"message": "Volley Club Platform API"}