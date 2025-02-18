# test_register.py
from app import bcrypt
import pytest

# test for good case
def test_register(client):  # `client` is passed as an argument
    response = client.post('/register',json={"username":"test_username","password":"test_password"})  # Simulates POST request to /register
    assert response.status_code == 201  # Check if status code is 200
    assert response.json == {"msg": "User registered successfully"}  # Check if response is correct

def test_wrong_request(client):  # `client` is passed as an argument
    response = client.get('/register')  # Simulates GET request to /register
    assert response.status_code == 405  # Check if status code is 405

# # test for bad case
# 1. test for missing or invalid JSON in request
def test_register_no_data(client):  # `client` is passed as an argument
    response = client.post('/register') # Simulates POST request to without any data
    assert response.status_code == 400 # Check if status code is 405
    assert response.json == {"msg": "Missing or invalid JSON in request",
                            "error": "Bad request"}  # Check if response is correct

# 2. test for password lennght
def test_register_password_len(client):  # `client` is passed as an argument
    response = client.post('/register',json={"username":"test_username","password":"password"}) # Simulates POST request to without any data
    assert response.status_code == 400 # Check if status code is 405
    assert response.json == {"msg": "Password shoud be longer then 10 characters",
                            "error": "Bad request"}  # Check if response is correct

# 3. test for username lennght
def test_register_username_len(client):  # `client` is passed as an argument
    response = client.post('/register',json={"username":"user","password":"test_password"})
    assert response.status_code == 400 # Check if status code is 400
    assert response.json == {"msg": "Username shoud be longer then 4 characters",
                            "error": "Bad request"}  # Check if response
    
# 4. test for missing username or password
@pytest.mark.parametrize("payload", [
    {"password": "test_password"},  # Missing username
    {"username": "test_username"}   # Missing password
])
def test_register_missing_parameter(client, payload):
    """Test registration fails when username or password is missing."""
    response = client.post('/register', json=payload)

    assert response.status_code == 400  # Check for Bad Request
    assert response.json == {
        "msg": "Username and password are required",
        "error": "Bad request"}  # Validate error message

def test_hash_is_different():
    password = "password123"
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    assert password != hashed_password  # Ensures plaintext is not stored

# Areas for Improvement:

# Username Already Exists: There's no test for the case where a username already exists (status code 409). You should add this test.
# Test for Good Case: Your test_register has a password that's shorter than 10 characters ("test_password"), but your validation requires passwords longer than 10 characters. This test will fail as written.
# Assertions: Some assertions have incorrect comments (e.g., checking for status code 400 but comment says 405).
# Database Interaction: You're not testing if the user is actually saved to the database. Consider adding a test that queries the database after registration.
