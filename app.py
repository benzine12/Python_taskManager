from datetime import datetime, timezone
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Task, User
from db import DB
import logging
from flask_jwt_extended import JWTManager, create_access_token
from config import Config
from flask_bcrypt import Bcrypt
from modules import get_current_user
import redis
import json

# Configure the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')

console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

# Create formatters and add them to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

app = Flask(__name__)

# App Configurations
app.config.from_object(Config)

CORS(app)
jwt = JWTManager(app)
DB.init_app(app)
bcrypt = Bcrypt(app)

# Initialize database tables
with app.app_context():
    DB.create_all()
    logger.info("Database tables initialized successfully!")

# Initialize Redis connection
redis_client = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    decode_responses=True  # decode to string
)

@app.post('/tasks')
@get_current_user
def new_task(user):
    data = request.json

    # Define allowed fields
    allowed_fields = {"task_name", "theme", "task_desc"}

    # Check for unexpected fields
    unexpected_fields = set(data.keys()) - allowed_fields
    if unexpected_fields:
        return jsonify({"error": f"Unexpected fields: {', '.join(unexpected_fields)}"}), 400

    # Validate required fields
    if not allowed_fields.issubset(data.keys()):
        return jsonify({"error": f"Missing required fields: {', '.join(allowed_fields - set(data.keys()))}"}), 400

    # Create the task
    add_task = Task(
        user_id=user.id,
        task_name=data["task_name"],
        theme=data["theme"],
        task_desc=data.get("task_desc"),
    )

    # Save to database
    DB.session.add(add_task)
    try:
        DB.session.commit()
    except Exception as e:
        DB.session.rollback()
        logger.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database error occurred"}), 500

    redis_client.delete(f"user:{user.id}:tasks")
    return jsonify({"message": "Task added successfully", "task": add_task.to_dict()}), 201

# endpoint show 1 task with the id
@app.get('/tasks/<int:id>')
@get_current_user
def show_task(user, id):
    cache_key = f"user:{user.id}:task:{id}"

    cached_task = redis_client.get(cache_key)
    if cached_task:  # Check if the task is cached in Redis
        logger.info(f"Task {id} for user {user.id} loaded from Redis cache.")
        return jsonify(json.loads(cached_task)), 200

    task = Task.active().filter_by(id=id, user_id=user.id).first()
    if task:
        task_dict = task.to_dict()
        redis_client.setex(cache_key, 60, json.dumps(task_dict))
        return jsonify(task.to_dict()), 200

    return jsonify({"message": "Task not found!"}), 404

# endpoint update the task
@app.put('/tasks/<int:id>')
@get_current_user
def update_task(user, id):
    data = request.json
    task = Task.active().filter_by(id=id, user_id=user.id).first()

    if task:
        allowed_fields = {"task_name", "theme", "task_desc", "status"}
        unexpected_fields = set(data.keys()) - allowed_fields
        if unexpected_fields:
            return jsonify({"error": f"Unexpected fields: {', '.join(unexpected_fields)}"}), 400

        # Convert status correctly if provided
        status = data.get("status", task.status)
        if isinstance(status, str):  # Convert string to boolean if necessary
            status = status.lower() == "true"

        # Prevent closing the task directly if not allowed
        if task.status is True and status is False:
            return jsonify({"message": "ERROR - first close the task properly!"}), 400

        # If task is reactivated (False → True), reset end_date
        if task.status is False and status is True:
            task.end_date = None

        # Update other fields
        task.task_name = data.get("task_name", task.task_name)
        task.theme = data.get("theme", task.theme)
        task.task_desc = data.get("task_desc", task.task_desc)
        task.status = status

        # Invalidate Redis cache for this task
        cache_key = f"user:{user.id}:task:{id}"
        redis_client.delete(cache_key)

        try:
            DB.session.commit()
        except Exception as e:
            DB.session.rollback()
            logger.error(f"Database error: {str(e)}")
            return jsonify({"error": "Database error occurred"}), 500

        redis_client.delete(f"user:{user.id}:tasks")
        return jsonify({"message": "Task updated successfully!", "task": task.to_dict()}), 200
    return jsonify({"message": "Task not found!"}), 404

# endpoint close the task
@app.put('/tasks/close/<int:id>')
@get_current_user
def close_task(user, id):
    task = Task.active().filter_by(id=id, user_id=user.id).first()

    if not task:
        return jsonify({"message": "There is no such task!"}), 404
    if task.status is False:
        return jsonify({"message": "Task already closed!"}), 400

    task.status = False
    task.end_date = datetime.now(timezone.utc)

    # Invalidate Redis cache for this task
    cache_key = f"user:{user.id}:task:{id}"
    redis_client.delete(cache_key)

    try:
        DB.session.commit()
    except Exception as e:
        DB.session.rollback()
        logger.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database error occurred"}), 500

    redis_client.delete(f"user:{user.id}:tasks")
    return jsonify({'message': 'Task closed successfully!', 'task': task.to_dict()}), 200

# endpoint to show all your tasks
@app.get('/tasks')
@get_current_user
def show_tasks(user):
    cache_key = f"user:{user.id}:tasks"
    cached_tasks = redis_client.get(cache_key)
    if cached_tasks:
        return jsonify(json.loads(cached_tasks)), 200

    user_tasks = Task.active().filter_by(user_id=user.id).all()
    tasks_list = [task.to_dict() for task in user_tasks]
    redis_client.setex(cache_key, 60, json.dumps(tasks_list))
    return jsonify(tasks_list), 200

@app.delete('/tasks/<int:id>')
@get_current_user
def delete_task(user, id):
    task = Task.active().filter_by(id=id, user_id=user.id).first()

    if not task:
        return jsonify({"message": "There is no such task!"}), 404
    if task.deleted:
        return jsonify({"message": "Task already deleted!"}), 400

    task.deleted = True
    task.deleted_at = datetime.now(timezone.utc)
    try:
        DB.session.commit()
    except Exception as e:
        DB.session.rollback()
        logger.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database error occurred"}), 500

    redis_client.delete(f"user:{user.id}:tasks")
    return jsonify({"message": "Task deleted successfully!", "task": task.to_dict()}), 200

# test endpoint
@app.get('/')
def main_page():
    return jsonify({'message': 'Flask run'}), 200

@app.post('/register')
# @func_logger
def register():
    '''Register func
        send username and password for register.'''
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing or invalid JSON in request",
                            "error": "Bad request"}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            return jsonify({"msg": "Username and password are required",
                            "error": "Bad request"}), 400

        if len(password) <= 10:
            return jsonify({"msg": "Password shoud be longer then 10 characters",
                            "error": "Bad request"}), 400

        if len(username) <= 4:
            return jsonify({"msg": "Username shoud be longer then 4 characters",
                            "error": "Bad request"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "Username already exists",
                            "error": "Something went wrong"}), 409

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)

        DB.session.add(new_user)
        try:
            DB.session.commit()
        except Exception as e:
            DB.session.rollback()
            logger.error(f"Database error: {str(e)}")
            return jsonify({"error": "Database error occurred"}), 500

        return jsonify({"msg": "User registered successfully"}), 201

# login func
@app.post('/login')
# @func_logger
def login():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing or invalid JSON in request",
                            "error": "Bad request"}), 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            return jsonify({"msg": "Username and password are required",
                            "error": "Bad request"}), 400

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.id))
            # refresh_token = create_refresh_token(identity=username)
            return jsonify({"msg": "Welcome back, commander!",
                            "access_token": access_token}), 200

        return jsonify({"msg": "Invalid username or password",
                        "error": "Something went wrong"}), 401

# starting point of the flask server
if __name__ == '__main__':
    with app.app_context():
        DB.create_all()
    app.run(debug=True, port=8000, host='0.0.0.0')