from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from db import DB
from models import User

def get_current_user(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()  # Now retrieving user ID instead of username
        user = DB.session.get(User, user_id)  # Query by primary key
        if not user:
            return jsonify({"msg": "User not found"}), 404
        return func(user, *args, **kwargs)  # Pass the user object to the original function
    return wrapper