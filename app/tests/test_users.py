import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from app.models.user import User

client = TestClient(app)

def test_get_user_profile():
    # First login to get token
    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "test123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Test getting user profile
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "username" in data
    assert "email" in data
    assert "full_name" in data

def test_update_user_profile():
    # First login to get token
    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "test123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Test updating user profile
    response = client.put(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "full_name": "Updated Test User",
            "email": "updated@example.com"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Test User"
    assert data["email"] == "updated@example.com"

def test_search_users():
    # First login to get token
    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "test123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Test searching users
    response = client.get(
        "/users/search?query=test",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
