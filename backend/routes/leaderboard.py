"""
Leaderboard routes
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from backend.models.user import User

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/')
@login_required
def index():
    """Leaderboard page showing top users by group"""
    # Get top 5 users in the current user's group
    top_users = User.query.filter_by(major_group=current_user.major_group)\
        .order_by(User.points.desc())\
        .limit(5)\
        .all()
    
    # Get user's rank
    user_rank = User.query.filter(
        User.major_group == current_user.major_group,
        User.points > current_user.points
    ).count() + 1
    
    return render_template('leaderboard/index.html',
                         top_users=top_users,
                         current_user=current_user,
                         user_rank=user_rank)
