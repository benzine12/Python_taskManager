# Task Management API

This project is a Task Management Application using Flask for backend and React for Frontend. It allows you to create, update, delete, and view tasks.

## Features

- login and registration
- Add new tasks
- Update existing tasks
- Delete tasks (soft delete)
- View tasks by status
- Close tasks
- REST API design

## Requirements

- Python 3.13
- Flask 3.1.0
- Flask-Cors 5.0.0
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.0.37
- pytest 8.3.4

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/benzine12/Python_taskManager
    cd Python_taskManager
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask server:
    ```sh
    python app.py
    ```

3. The API will be available at `http://127.0.0.1:5001/`.

## API Endpoints
- `GET /` - Test endpoint to check if Flask run
- `POST /tasks` - Add a new task
- `GET /tasks/<int:id>` - View a task by ID
- `PUT /tasks/<int:id>` - Update a task
- `PUT /tasks/close/<int:id>` - Close a task
- `GET /tasks` - View all tasks
- `DELETE /tasks/delete/<int:id>` - Delete a task(soft delete)
- `POST /register` - Register new user
- `POST /login` - Login and Get JWT 


## Running Tests

To run the tests, use the following command:
```sh
pytest
