# good case
def test_update_task(client,jwt_header,test_task):
    response = client.put('/tasks/1',headers=jwt_header,json={
        "task_name":"updated_task",
        "theme":"updatex_theme",
        "task_desc":"updated_desc"
    })

    assert response.status_code == 200
    assert response.json["message"] == "Task updated successfully!"
    assert response.json["task"]["task_name"] == "updated_task"
    assert response.json["task"]["theme"] == "updatex_theme"
    assert response.json["task"]["task_desc"] == "updated_desc"

# wrong user
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

    response = client.put('/tasks/1',headers=headers_B,json={
        "task_name":"updated_task",
        "theme":"updatex_theme",
        "task_desc":"updated_desc"
    })

    assert response.status_code == 404
    assert response.json == {"message": "Task not found!"}

# wrong id
def test_wrong_id(client,jwt_header,test_task):
    response = client.put('/tasks/2',headers=jwt_header,json={
        "task_name":"updated_task",
        "theme":"updatex_theme",
        "task_desc":"updated_desc"
    })

    assert response.status_code == 404
    assert response.json == {"message": "Task not found!"}

# test no data
def test_wrong_id(client,jwt_header,test_task):
    response = client.put('/tasks/1',headers=jwt_header)

    assert response.status_code == 415


# unexpected_fields
def test_unexpected_fields(client,jwt_header,test_task):
    response = client.put('/tasks/1',headers=jwt_header,json={
        "task_name":"updated_task",
        "theme":"updatex_theme",
        "task_desc":"updated_desc",
        "TASK_UNEXPECTED":"updated_UNEXPECTED"
    })

    assert response.status_code == 400
    assert response.json["error"] == "Unexpected fields: TASK_UNEXPECTED"

# check task closing 100-102
def test_closed_task(client,jwt_header,test_task):
    response = client.put('/tasks/1',headers=jwt_header,json={
        "status":False
    })

    assert response.status_code == 400
    assert response.json == {"message": "ERROR - first close the task properly!"}

# check if task reactivating 105-106

