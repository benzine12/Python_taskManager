import pytest
from app import app, DB
from models import Task

# Configure the app for testing
@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = False

    with app.app_context():
        DB.create_all()  # Creates tables in the test database
        yield app.test_client()
        DB.drop_all()  # Cleans up after tests

# Test that always passes
def test_always_passes():
    assert True

def test_new_task(test_client):
    new_task_data  ={
        'task_name': 'Test task',
        'theme': 'Testing',
        'task_desc': 'test task description'
    }

    # send the data to the endpoint
    response = test_client.post('/tasks', json=new_task_data)

    # check if the response is correct
    assert response.status_code == 201
    assert response.json == {'message':'task added'}

    # verify the data in the database
    with app.app_context():
        task = Task.query.filter_by(task_name='Test task').first()
        assert task
        assert task.task_name == "Test task"
        assert task.theme == 'Testing'
        assert task.task_desc == 'test task description'

def test_show_task(test_client):
    # Step 1: Add a test task to the database
    test_task_data = {
        "task_name": "Test Task",
        "theme": "Test Theme",
        "task_desc": "This is a test task description."
    }
    response = test_client.post('/tasks', json=test_task_data)
    assert response.status_code == 201  # Ensure task is added

    # Step 2: Get the ID of the added task
    with app.app_context():
        task = Task.query.filter_by(task_name="Test Task").first()
        task_id = task.id  # Retrieve the ID of the task

    # Step 3: Test the endpoint to fetch the task by ID
    response = test_client.get(f'/tasks/{task_id}')
    assert response.status_code == 200  # Check if the request is successful

    # Step 4: Verify the response data
    data = response.json
    assert isinstance(data, list)  # Check if the response is a list
    assert len(data) == 1  # Ensure only one task is returned
    task_data = data[0]
    assert task_data['task_name'] == "Test Task"
    assert task_data['theme'] == "Test Theme"
    assert task_data['task_desc'] == "This is a test task description."

def test_show_task_not_found(test_client):
    # Test with a non-existent task ID
    response = test_client.get('/tasks/9999')  # Use an ID that doesn't exist
    assert response.status_code == 404  # Check if the status code is 404
    assert response.json['message'] == "Task not found!"




if __name__ == '__main__':
    pytest.main()