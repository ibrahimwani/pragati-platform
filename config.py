# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGODB_URI', 'mongodb://localhost:27017/pragati')
    }
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    USE_GEMINI = os.getenv('USE_GEMINI', 'False').lower() == 'true'
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')