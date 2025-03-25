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