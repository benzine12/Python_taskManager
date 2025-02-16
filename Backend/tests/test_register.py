# test_register.py

# test for good case
def test_register(client):  # `client` is passed as an argument
    response = client.post('/register',json={"username":"test_username","password":"test_password"})  # Simulates POST request to /register
    assert response.status_code == 201  # Check if status code is 200
    assert response.json == {"msg": "User registered successfully"}  # Check if response is correct

# # test for bad case
# 1. test for missing or invalid JSON in request
def test_register_no_data(client):  # `client` is passed as an argument
    response = client.post('/register') # Simulates POST request to without any data
    assert response.status_code == 400 # Check if status code is 405
    assert response.json == {"msg": "Missing or invalid JSON in request",
                            "error": "Bad request"}  # Check if response is correct

