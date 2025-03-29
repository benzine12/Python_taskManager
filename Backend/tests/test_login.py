# test_login.py

def test_login(client,test_user):
    # Good case
    response = client.post('/login',
                          json={"username": test_user["username"], 
                                "password": test_user["password"]})

    assert response.status_code == 200 
    assert response.json["msg"] == "Welcome back, commander!"
    assert "access_token" in response.json

def test_login_invalid_method(client,test_user):
    response = client.get('/login',
                          json={"username": test_user["username"], 
                                "password": test_user["password"]})
    
    assert response.status_code == 405

def test_login_invalid_request(client):
    response = client.post('/login')

    assert response.status_code == 400
    assert response.json == {"msg": "Missing or invalid JSON in request",
                            "error": "Bad request"}

def test_login_missing_credits(client,test_user):
    response = client.post('/login',
                           json={"username":test_user["username"]})
    
    assert response.status_code == 400
    assert response.json == {"msg": "Username and password are required",
                            "error": "Bad request"}
    
def test_login_invalid_credits(client,test_user):
        response = client.post('/login',
                          json={"username": "username123", 
                                "password": "username123"})
        
        assert response.status_code == 401
        assert response.json == {"msg": "Invalid username or password",
                        "error": "Something went wrong"}
        
