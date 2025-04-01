# good case
def test_show_task(client,jwt_header,test_task):
    response = client.get('/tasks/1',headers=jwt_header)

    assert response.status_code == 200
    assert response.json["task_name"] == "test_task"

# test to try show task of another user
def test_wrong_user(client, jwt_header):
    """Ensure that user A cannot view tasks created by user B.
        User A - created by jwt_header fixture
        User B - will be created manually """
        
    # Simulates POST request to /register
    client.post('/register',
               json={"username":"test_user_B","password":"test_password"})
    
    # Simulate POST request to /login
    login_user_B = client.post('/login',
                          json={"username": "test_user_B", 
                                "password": "test_password"})
    
    headers_B = {"Authorization": f"Bearer {login_user_B.json["access_token"]}"}

    response = client.get('/tasks/1',headers=headers_B)

    assert response.status_code == 404
    assert response.json == {"message": "Task not found!"}

# test wrong task id
def test_wrong_id(client,jwt_header,test_task):
    response = client.get('/tasks/2',headers=jwt_header)

    assert response.status_code == 404
    assert response.json == {"message": "Task not found!"}