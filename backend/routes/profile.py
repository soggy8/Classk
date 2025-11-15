"""
Profile routes
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from backend.models.mission import Mission

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/')
@login_required
def index():
    """User profile page"""
    # Get user's created missions
    created_missions = Mission.query.filter_by(creator_id=current_user.id)\
        .order_by(Mission.created_at.desc()).all()
    
    # Get user's accepted/completed missions
    accepted_missions = Mission.query.filter_by(assignee_id=current_user.id)\
        .order_by(Mission.created_at.desc()).all()
    
    completed_missions = [m for m in accepted_missions if m.status == Mission.STATUS_COMPLETED]
    
    return render_template('profile/index.html',
                         user=current_user,
                         created_missions=created_missions,
                         accepted_missions=accepted_missions,
                         completed_missions=completed_missions)
