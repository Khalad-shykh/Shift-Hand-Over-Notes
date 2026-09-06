import pytest
from app import app, notes


@pytest.fixture
def client():
    notes.clear()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_add_note(client):
    response = client.post(
        "/notes",
        json={
            "home_id": "home-1",
            "author": "Robert William",
            "body": "The resident needs safeguarding from neglect and physical injury.",
        },
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["home_id"] == "home-1"
    assert data["author"] == "Robert William"
    assert data["id"] == 1
    assert data["severity"] == "high"


def test_add_note_failed(client):
    response = client.post(
        "/notes",
        json={
            "home_id": "home-1",
            "body": "The resident needs safeguarding from neglect and physical injury.",
        },
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "author" in data["error"]
