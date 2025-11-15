"""
Routes initialization
"""
from backend.routes.auth import auth_bp
from backend.routes.missions import missions_bp
from backend.routes.profile import profile_bp
from backend.routes.leaderboard import leaderboard_bp
from backend.routes.admin import admin_bp

__all__ = ['auth_bp', 'missions_bp', 'profile_bp', 'leaderboard_bp', 'admin_bp']
