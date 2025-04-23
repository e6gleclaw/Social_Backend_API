import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from app.models.user import User
from app.models.friend import Friend

client = TestClient(app)

def test_send_friend_request():
    # First login to get token
    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "test123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Test sending friend request
    response = client.post(
        "/friends/request/2",  # Assuming user with ID 2 exists
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"

def test_accept_friend_request():
    # First login to get token
    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser2",  # Assuming this is the recipient
            "password": "test123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Test accepting friend request
    response = client.post(
        "/friends/accept/1",  # Assuming request ID 1 exists
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "accepted"

def test_get_friends_list():
    # First login to get token
    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "test123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Test getting friends list
    response = client.get(
        "/friends",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_remove_friend():
    # First login to get token
    login_response = client.post(
        "/auth/login",
        data={
            "username": "testuser",
            "password": "test123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Test removing friend
    response = client.delete(
        "/friends/2",  # Assuming friend with ID 2 exists
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Friend removed successfully"
