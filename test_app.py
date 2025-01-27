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

def test_add_task(test_client):
    # prepare the data for the new task
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

if __name__ == '__main__':
    pytest.main()