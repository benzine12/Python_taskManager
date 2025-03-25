# test_login.py
from flask_jwt_extended import create_access_token

def test_login(client):
    response = client.post('/login', # Simulates POST request to /register
    json={"username":"test_username","password":"test_password"})

    assert response.status_code == 201  # Check if status code is 201
    # assert response.json == {"msg": "Welcome back, commander!",
    #                          "access_token": create_access_token(identity=str('test_username'))}