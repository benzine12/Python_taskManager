# good case
def test_new_task(client,jwt_header):
    response = client.post('/tasks',headers=jwt_header,json={
        "task_name":"test_task",
        "theme":"test_theme",
        "task_desc":"test_desc"
    })

    assert response.status_code == 201
    assert response.json["message"] == "Task added successfully"

# bad case

def test_unexpected_fields(client,jwt_header):
    response = client.post('/tasks',headers=jwt_header,json={
        "task_name":"test_task",
        "theme":"test_theme",
        "TASK_ROLE":"test_desc"
    })

    assert response.status_code == 400
    assert response.json["error"] == "Unexpected fields: TASK_ROLE"

def test_missing_fields(client,jwt_header):
    response = client.post('/tasks',headers=jwt_header,json={
        "task_name":"test_task",
        "theme":"test_theme"
    })

    assert response.status_code == 400
    assert response.json["error"] == "Missing required fields: task_desc"