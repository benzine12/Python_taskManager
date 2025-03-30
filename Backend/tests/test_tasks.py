def test_new_task(client,jwt_header):
    response = client.post('/tasks',headers=jwt_header,json={
        "task_name":"test_task",
        "theme":"test_theme",
        "task_desc":"test_desc"
    })

    assert response.status_code == 201