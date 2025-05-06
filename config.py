import os
from dotenv import load_dotenv

# Load environment variables from a .env file, if available
load_dotenv()

class Config:
    # Securely load secret key from environment variables, or use a fallback key
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')  # Replace 'fallback-secret-key' for production use
    
    # Get the base directory where this file is located
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Set database URI to point to the SQLite database in the instance folder
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"
    
    # Prevent SQLAlchemy from tracking object changes to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Additional configurations can go here, such as logging or email settings

