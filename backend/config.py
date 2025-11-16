"""
Configuration settings for the Classk Flask application
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{BASE_DIR / "classk.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
    STATIC_FOLDER = BASE_DIR / 'frontend'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # Pagination
    POSTS_PER_PAGE = 10
    
    # Points configuration
    POINTS_HELP_EASY = 20
    POINTS_HELP_MEDIUM = 40
    POINTS_HELP_HARD = 60
    POINTS_LOST_FOUND = 30
    POINTS_TEAM_STUDY = 20
    
    # Level calculation (every 100 points = 1 level)
    POINTS_PER_LEVEL = 100
    
    # Available majors/groups
    AVAILABLE_MAJORS = [
        'Computer Science',
        'Engineering',
        'Business Administration',
        'Medicine',
        'Law',
        'Arts & Humanities',
        'Science',
        'Education',
        'Psychology',
        'Social Sciences',
        'Mathematics',
        'Physics',
        'Chemistry',
        'Biology',
        'Economics',
        'Communications',
        'Architecture',
        'Other'
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
