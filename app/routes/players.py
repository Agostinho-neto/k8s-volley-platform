# app/routes/players.py

import logging

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.player import create_player as create_player_repository
from app.repositories.player import delete_player as delete_player_repository
from app.repositories.player import get_player_by_id as get_player_by_id_repository
from app.repositories.player import list_players as list_players_repository
from app.repositories.player import update_player as update_player_repository
from app.schemas.player import PlayerCreate, PlayerResponse, PlayerUpdate

router = APIRouter()
logger = logging.getLogger("volleyops.players")


def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", "unknown")


@router.post(
    "/players",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_player(
    player: PlayerCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    created_player = create_player_repository(db, player)

    logger.info(
        "player_created",
        extra={
            "extra_fields": {
                "event": "player_created",
                "request_id": get_request_id(request),
                "player_id": created_player.id,
                "name": created_player.name,
                "number": created_player.number,
                "position": created_player.position,
            }
        },
    )
    return created_player


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
    request: Request,
    db: Session = Depends(get_db),
):
    db_player = get_player_by_id_repository(db, player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    old_values = {
        "name": db_player.name,
        "position": db_player.position,
        "number": db_player.number,
    }

    new_values = player.model_dump()

    changes = {
        field: {
            "old": old_values[field],
            "new": new_values[field],
        }
        for field in new_values
        if old_values[field] != new_values[field]
    }

    updated_player = update_player_repository(db, db_player, player)

    logger.info(
        "player_updated",
        extra={
            "extra_fields": {
                "event": "player_updated",
                "request_id": get_request_id(request),
                "player_id": updated_player.id,
                "changes": changes,
            }
        },
    )
    return updated_player


@router.delete("/players/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(
    player_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    db_player = get_player_by_id_repository(db, player_id)
    if db_player is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found",
        )

    deleted_player = {
        "id": db_player.id,
        "name": db_player.name,
        "position": db_player.position,
        "number": db_player.number,
    }

    delete_player_repository(db, db_player)
    logger.info(
        "player_deleted",
        extra={
            "extra_fields": {
                "event": "player_deleted",
                "request_id": get_request_id(request),
                "player": deleted_player,
            }
        },
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
