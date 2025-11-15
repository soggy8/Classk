"""
Flask application factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pathlib import Path
from backend.config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    """Application factory function"""
    # Get absolute paths
    base_dir = Path(__file__).parent.parent
    template_dir = base_dir / 'templates'
    static_dir = base_dir / 'frontend'
    
    app = Flask(__name__, 
                template_folder=str(template_dir),
                static_folder=str(static_dir),
                static_url_path='/static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.missions import missions_bp
    from backend.routes.profile import profile_bp
    from backend.routes.leaderboard import leaderboard_bp
    from backend.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(missions_bp, url_prefix='/missions')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Register user loader
    from backend.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register root route
    from flask import render_template
    
    @app.route('/')
    def index():
        """Home page route"""
        return render_template('index.html')
    
    return app
