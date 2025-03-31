# conftest.py
import pytest
from app import app, DB

@pytest.fixture
def client():
    """Creates a test client for the Flask app."""
    app.config['TESTING'] = True  # Enables testing mode
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        DB.create_all()  # Create tables before tests

    with app.test_client() as client:
        yield client  # Provides the test client for tests
    
    with app.app_context():
        DB.drop_all()

@pytest.fixture
def test_user(client, username: str = "test_username",password: str = "test_password"):
    """Create test user in database to test the different functions"""
    response = client.post('/register', # Simulates POST request to /register
                           json={"username":username,"password":password})
    
    assert response.status_code == 201
    assert response.json == {"msg": "User registered successfully"}

    return {"username":username,"password":password}

@pytest.fixture
def jwt_header(client,test_user):
    response = client.post('/login',
                          json={"username": test_user["username"], 
                                "password": test_user["password"]})
    
    token = response.json["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers

@pytest.fixture
def test_task(client,jwt_header):
    response = client.post('/tasks',headers=jwt_header,json={
        "task_name":"test_task",
        "theme":"test_theme",
        "task_desc":"test_desc"
    })
    return {
        "task_name":"test_task",
        "theme":"test_theme",
        "task_desc":"test_desc"
    }