# test_register.py
from app import User
from app import bcrypt
import pytest

# test for good case
def test_register(client):  # `client` is passed as an argument
    response = client.post('/register', # Simulates POST request to /register
                           json={"username":"test_username","password":"test_password"})
    assert response.status_code == 201  # Check if status code is 201
    assert response.json == {"msg": "User registered successfully"}  # Check if response is correct

def test_wrong_request(client):  # `client` is passed as an argument
    response = client.get('/register')  # Simulates GET request to /register
    assert response.status_code == 405  # Check if status code is 405

# # test for bad case
# 1. test for missing or invalid JSON in request
def test_register_no_data(client):  # `client` is passed as an argument
    response = client.post('/register') # Simulates POST request to without any data
    assert response.status_code == 400 # Check if status code is 400
    assert response.json == {"msg": "Missing or invalid JSON in request",
                            "error": "Bad request"}  # Check if response is correct

# 2. test for password lennght
def test_register_password_len(client):  # `client` is passed as an argument
    response = client.post('/register',json={"username":"test_username","password":"password"}) # Simulates POST request to without any data
    assert response.status_code == 400 # Check if status code is 400
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

# 5. test is password encrypted
def test_hash_is_different():
    password = "password123"
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    assert password != hashed_password  # Ensures plaintext is not stored

# 6. test is user already exist
def test_user_already_exists(client):
    response = client.post('/register',json={"username":"test_username","password":"test_password"})  # Simulates POST request to /register
    assert response.status_code == 201  # Check if status code is 201
    assert response.json == {"msg": "User registered successfully"}  # Check if response is correct

    response = client.post('/register',json={"username":"test_username","password":"test_password"})  # Simulates POST request to /register
    assert response.status_code == 409  # Check if status code is 409
    assert response.json == {"msg": "Username already exists",
                            "error": "Something went wrong"}  # Check if response is correct

# 7 . test if user added to database
def test_database_interaction(client):
    response = client.post('/register',json={"username":"test_username","password":"test_password"})  # Simulates POST request to /register

    assert response.status_code == 201  # Check if status code is 201
    assert response.json == {"msg": "User registered successfully"}  # Check if response is correct
   
    assert User.query.filter_by(username="test_username").first() is not None

