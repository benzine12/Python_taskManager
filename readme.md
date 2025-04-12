# Task Management API

This project is a Task Management Application using Flask. It allows you to create, update, delete, and view tasks.

## Features

- User authentication with JWT tokens
- Secure password hashing with bcrypt
- Add new tasks with name, theme, and description
- Update existing tasks
- Delete tasks (soft delete)
- View tasks by status
- Close tasks with automatic timestamp
- REST API design
- Comprehensive logging system
- PostgreSQL database integration
- CORS support for frontend integration
- Docker compose to fast deploy

## Requirements

- Python 3.13
- Flask 3.0.2
- Flask-CORS 4.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-JWT-Extended 4.6.0
- Flask-Bcrypt 1.0.1
- Flask-Redis 0.4.0
- SQLAlchemy 2.0.27
- psycopg2-binary 2.9.9
- pytest 8.3.4
- python-dotenv 1.0.1
- Redis 5.0.1
- pika 1.3.2

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

## Installation with Docker compose
  ```sh
    docker compose up
  ```


## Usage

1. Run the Flask server:
  ```sh
    python app.py
  ```

2. The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

### Authentication
- `POST /register` - Register new user
  - Required fields: username (min 4 chars), password (min 10 chars)
- `POST /login` - Login and Get JWT token
  - Required fields: username, password

### Tasks
- `GET /` - Test endpoint to check if Flask is running
- `POST /tasks` - Add a new task
  - Required fields: task_name, theme, task_desc
- `GET /tasks/<int:id>` - View a task by ID
- `PUT /tasks/<int:id>` - Update a task
  - Optional fields: task_name, theme, task_desc, status
- `PUT /tasks/close/<int:id>` - Close a task
- `GET /tasks` - View all tasks for the current user
- `DELETE /tasks/<int:id>` - Delete a task (soft delete)

Note: All task endpoints require JWT authentication. Include the token in the Authorization header as "Bearer <token>"

## Running Tests

To run the tests, use the following command:
```sh
coverage run -m pytest
coverage report -m    
```

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Input validation and sanitization
- Soft delete for tasks
- Protected routes with user-specific access
- CORS protection
- Comprehensive error handling