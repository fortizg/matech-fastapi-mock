import pytest
from fastapi.testclient import TestClient
from app import app, users_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():
    # Reset the database before each test
    users_db.clear()
    users_db.extend(
        [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
        ]
    )


def test_get_users():
    response = client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "John Doe"
    assert response.json()[1]["name"] == "Jane Smith"


def test_create_user():
    new_user = {"name": "Alice Johnson", "email": "alice@example.com"}
    response = client.post("/api/users", json=new_user)
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["name"] == new_user["name"]
    assert created_user["email"] == new_user["email"]
    assert "id" in created_user


def test_get_user():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"


def test_get_nonexistent_user():
    response = client.get("/api/users/999")
    assert response.status_code == 404


def test_create_user_invalid_email():
    new_user = {"name": "Invalid User", "email": "not-an-email"}
    response = client.post("/api/users", json=new_user)
    assert response.status_code == 422  # Unprocessable Entity


def test_create_duplicate_user():
    existing_user = {"name": "John Doe", "email": "john@example.com"}
    response = client.post("/api/users", json=existing_user)
    assert response.status_code == 200  # FastAPI allows duplicate users by default
    # If you implement duplicate checking, you might want to change this test
