from datetime import timedelta
import os

class Config:
    # Postgresql configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@postgresql:5432/taskmanager')
    DB_PORT = os.getenv('DB_PORT', '5432')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = 'YOUR_SUPER_SECRET_PASSWORD'
    JWT_ALGORITHM = "HS256"
    JWT_TOKEN_LOCATION = ["headers"]
    
    # Additional security settings
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  
    JWT_HEADER_TYPE = "Bearer" 
    JWT_HEADER_NAME = "Authorization" 

    # Redis configuration
    REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)

