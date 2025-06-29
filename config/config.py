import os
from dotenv import load_dotenv

load_dotenv()  # this must be above the Config class

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False