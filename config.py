import os

# Get the absolute folder path of this main directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-later")
    
    # 🔒 SECURE LOCAL SQLITE PATHWAY BINDING - REMOTE MYSQL LOOPS BYPASSED
    # Forced straight to its own local app.db file inside the instance directory
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Standard application upload directories configurations
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
