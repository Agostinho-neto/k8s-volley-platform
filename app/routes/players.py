# app/routes/players.py

from fastapi import APIRouter
from app.schemas.player import Player

router = APIRouter()

players_db = []

@router.post("/players")
def create_player(player: Player):
    players_db.append(player)
    return {
        "message": "Player created successfully",
        "player": player
    }

@router.get("/players")
def list_players():
    return players_db