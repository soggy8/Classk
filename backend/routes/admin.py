"""
Admin routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from backend import db
from backend.models.mission import Mission
from backend.models.user import User

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin access"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    # Get filter parameters
    category = request.args.get('category')
    status = request.args.get('status')
    creator_id = request.args.get('creator_id', type=int)
    
    # Query missions in admin's group with relationships
    query = Mission.query.options(
        joinedload(Mission.creator),
        joinedload(Mission.assignee)
    ).filter_by(group_name=current_user.major_group)
    
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    if creator_id:
        query = query.filter_by(creator_id=creator_id)
    
    missions = query.order_by(Mission.created_at.desc()).all()
    
    # Get all users in the group for filter
    group_users = User.query.filter_by(major_group=current_user.major_group).all()
    
    return render_template('admin/dashboard.html',
                         missions=missions,
                         group_users=group_users,
                         current_category=category,
                         current_status=status,
                         current_creator_id=creator_id)

@admin_bp.route('/invalidate/<int:mission_id>', methods=['POST'])
@login_required
@admin_required
def invalidate_points(mission_id):
    """Invalidate points for a completed mission"""
    mission = Mission.query.get_or_404(mission_id)
    
    if mission.group_name != current_user.major_group:
        flash('You can only invalidate points for missions in your group.', 'error')
        return redirect(url_for('admin.dashboard'))
    
    if mission.invalidate_points():
        flash('Points invalidated successfully.', 'success')
    else:
        flash('Failed to invalidate points.', 'error')
    
    return redirect(url_for('admin.dashboard'))
