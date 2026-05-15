# app/routes/players.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.player import create_player as create_player_repository
from app.repositories.player import list_players as list_players_repository
from app.schemas.player import PlayerCreate, PlayerResponse

router = APIRouter()


@router.post(
    "/players",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    return create_player_repository(db, player)


@router.get("/players", response_model=list[PlayerResponse])
def list_players(db: Session = Depends(get_db)):
    return list_players_repository(db)
