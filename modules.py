import logging
import functools
from collections import defaultdict
import random
import time
from models import IPAddres
from db import DB

# add to blacklist
def blacklist_ip(ip_address):
    try:
        # Check if the IP address already exists in the database
        existing_ip = IPAddres.query.filter_by(ip_address=ip_address).first()
        if existing_ip:
            if not existing_ip.blacklist:
                existing_ip.blacklist = True
                DB.session.commit()
                logging.info(f"IP {ip_address} blacklisted.")
        else:
            # Add the new IP address to the database
            new_ip = IPAddres(ip_address=ip_address, blacklist=True)
            DB.session.add(new_ip)
            DB.session.commit()
            logging.info(f"IP {ip_address} added to the blacklist.")
    except Exception as e:
        logging.error(f"Error blacklisting IP {ip_address}: {e}")

logger = logging.getLogger(__name__)

# Global error counter
error_counts = defaultdict(lambda: {"401": 0})
ip_409_counts = defaultdict(int)

MAX_ERROR_COUNT = 3

random_error_list = [
            ({"msg": "Missing or invalid JSON in request", "error": "Bad request"}, 400),
            ({"msg": "Username and password are required", "error": "Bad request"}, 400),
            ({"msg": "Invalid username or password", "error": "Something went wrong"}, 401),
            ({"msg": "Username already exists", "error": "Something went wrong"}, 409),
            ({"msg": "Username or password shouldn't be longer than 10 characters", "error": "Bad request"}, 400),]
        
error_response, status_code = random.choice(random_error_list)

def func_logger(func):
    """
    Python decorator function, FuncLogger,
    which adds logging functionality to any function it wraps.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        username = None

        # Attempt to log the username if available in the request
        try:
            from flask import request,jsonify

            blacklisted_ip = IPAddres.query.filter_by(ip_address=request.remote_addr, blacklist=True).first()
            if blacklisted_ip:
                logging.warning(f"Blocked request from blacklisted IP: {request.remote_addr}")
                time.sleep(random.randrange(8))
                # return jsonify(random_error_list[2][0]), random_error_list[2][1]
                error_response, status_code = random.choice(random_error_list)
                return jsonify(error_response), status_code
            
            if request.is_json:
                username = request.json.get('username', None)
                if username:
                    logging.info(f"Username provided: {username}")
                else:
                    logging.warning("Username not found in JSON.")
            else:
                logging.warning("Request is not JSON.")
        except Exception as e:
            logging.warning(f"Could not extract username: {e}")

        try:
            # Execute the function
            result = func(*args, **kwargs)

            # Check for tuple response (Response object, status_code)
            from flask import Response
            status_code = None
            if isinstance(result, tuple):
                response, status_code = result
                # logging.debug(f"Response is a tuple: {response}, {status_code}")
            elif isinstance(result, Response):
                response = result
                status_code = response.status_code
            else:
                response = result

            # Handle error status codes
            if status_code == 401 and username:
                error_counts[username]["401"] += 1
                print(f"401 Count for {username}: {error_counts[username]['401']}")
                if error_counts[username]["401"] >= MAX_ERROR_COUNT:
                    logging.critical(f'''Potential BruteForce attack detected
                    username - {username}from the IP - {request.remote_addr}''')
                    blacklist_ip(request.remote_addr)

            elif status_code == 409 and request.remote_addr:
                ip_409_counts[request.remote_addr] += 1
                print(f'''409 Count for IP {request.remote_addr}:
                       {ip_409_counts[request.remote_addr]}''')
                if ip_409_counts[request.remote_addr] >= MAX_ERROR_COUNT:
                    logging.critical(f'''Potential Username Scraping detected :
                      username - {username} from the IP - {request.remote_addr}''')
                    blacklist_ip(request.remote_addr)

            # Log the return value
            logging.info(f"{func.__name__} returned {response} with status {status_code}")
            return result
        except Exception as e:
            # Log any exceptions raised during function execution
            logging.error(f"{func.__name__} raised an exception: {e}")
            raise  # Re-raise the exception for proper handling
    return wrapper


from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import User  # Import User model

def get_current_user(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()  # Now retrieving user ID instead of username
        user = User.query.get(user_id)  # Query by primary key
        if not user:
            return jsonify({"msg": "User not found"}), 404
        return func(user, *args, **kwargs)  # Pass the user object to the original function
    return wrapper