from sqlalchemy.orm import Session

from app.models.player import Player
from app.schemas.player import PlayerCreate


def create_player(db: Session, player: PlayerCreate) -> Player:
    db_player = Player(**player.model_dump())

    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return db_player


def list_players(db: Session) -> list[Player]:
    return db.query(Player).order_by(Player.id).all()


def get_player_by_id(db: Session, player_id: int) -> Player | None:
    return db.query(Player).filter(Player.id == player_id).first()
