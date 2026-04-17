from fastapi.testclient import TestClient
from main import app
import uuid
client = TestClient(app)
TEST_USER = f"test_{uuid.uuid4().hex[:8]}"

def test_register():
    response = client.post("/register", json={"username": TEST_USER, "password": "12345678"})
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully!"

def test_login():
    response = client.post("/login", data={"username":TEST_USER, "password": "12345678"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    
def test_register_duplicate():
    client.post("/register", json={"username": "duplicate_user", "password": "12345678"})
    response = client.post("/register", json={"username": "duplicate_user", "password": "12345678"})
    assert response.status_code == 400  # or 500

def test_login_wrong_password():
    response = client.post("/login", data={"username":TEST_USER, "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid password!"

    
def test_login_not_found():
    response = client.post("/login", data={"username":"AdminTester", "password": "12345678"})
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found!"
