# app/routes/players.py

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.player import create_player as create_player_repository
from app.repositories.player import delete_player as delete_player_repository
from app.repositories.player import get_player_by_id as get_player_by_id_repository
from app.repositories.player import list_players as list_players_repository
from app.repositories.player import update_player as update_player_repository
from app.schemas.player import PlayerCreate, PlayerResponse, PlayerUpdate

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


@router.get("/players/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = get_player_by_id_repository(db, player_id)
    if player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    return player


@router.put("/players/{player_id}", response_model=PlayerResponse)
def update_player(
    player_id: int,
    player: PlayerUpdate,
    db: Session = Depends(get_db),
):
    db_player = get_player_by_id_repository(db, player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    return update_player_repository(db, db_player, player)


@router.delete("/players/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    db_player = get_player_by_id_repository(db, player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    delete_player_repository(db, db_player)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
