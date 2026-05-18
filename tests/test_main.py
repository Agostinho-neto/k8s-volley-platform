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
    assert "text/html" in response.headers["content-type"]


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


def test_get_player_by_id():
    with TestClient(app) as client:
        created = client.post(
            "/players",
            json={
                "name": "Joao Silva",
                "position": "Levantador",
                "number": 10,
            },
        )
        response = client.get(f"/players/{created.json()['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == "Joao Silva"


def test_update_player():
    with TestClient(app) as client:
        created = client.post(
            "/players",
            json={
                "name": "Joao Silva",
                "position": "Levantador",
                "number": 10,
            },
        )
        response = client.put(
            f"/players/{created.json()['id']}",
            json={
                "name": "Maria Souza",
                "position": "Oposto",
                "number": 7,
            },
        )

    assert response.status_code == 200
    assert response.json()["name"] == "Maria Souza"
    assert response.json()["position"] == "Oposto"
    assert response.json()["number"] == 7


def test_delete_player():
    with TestClient(app) as client:
        created = client.post(
            "/players",
            json={
                "name": "Joao Silva",
                "position": "Levantador",
                "number": 10,
            },
        )
        player_id = created.json()["id"]
        delete_response = client.delete(f"/players/{player_id}")
        get_response = client.get(f"/players/{player_id}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_update_player_not_found():
    with TestClient(app) as client:
        response = client.put(
            "/players/999",
            json={
                "name": "Maria Souza",
                "position": "Oposto",
                "number": 7,
            },
        )

    assert response.status_code == 404


def test_delete_player_not_found():
    with TestClient(app) as client:
        response = client.delete("/players/999")

    assert response.status_code == 404
