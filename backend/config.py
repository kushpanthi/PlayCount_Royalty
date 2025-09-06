import os

class Config:
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
