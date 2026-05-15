import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_volleyops.db")

import pytest
from fastapi.testclient import TestClient

import app.models.player  # noqa: F401
from app.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200


def test_create_player():
    with TestClient(app) as client:
        response = client.post(
            "/players",
            json={
                "name": "Joao Silva",
                "position": "Levantador",
                "number": 10,
            },
        )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["name"] == "Joao Silva"
    assert response.json()["position"] == "Levantador"
    assert response.json()["number"] == 10
    assert "created_at" in response.json()
    assert "updated_at" in response.json()


def test_list_players():
    with TestClient(app) as client:
        client.post(
            "/players",
            json={
                "name": "Joao Silva",
                "position": "Levantador",
                "number": 10,
            },
        )
        response = client.get("/players")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Joao Silva"


def test_create_player_validates_number():
    with TestClient(app) as client:
        response = client.post(
            "/players",
            json={
                "name": "Joao Silva",
                "position": "Levantador",
                "number": 0,
            },
        )

    assert response.status_code == 422
