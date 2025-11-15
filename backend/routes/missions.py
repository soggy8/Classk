"""
Mission routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from backend import db
from backend.models.mission import Mission
from backend.models.user import User
from backend.config import Config

missions_bp = Blueprint('missions', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@missions_bp.route('/')
def list_missions():
    """List all missions"""
    category = request.args.get('category')
    status = request.args.get('status')
    
    if current_user.is_authenticated:
        query = Mission.query.filter_by(group_name=current_user.major_group)
    else:
        # For non-authenticated users, show all missions (or none)
        query = Mission.query.filter(False)  # Show no missions for non-authenticated users
    
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    
    missions = query.order_by(Mission.created_at.desc()).all()
    
    return render_template('missions/list.html', 
                         missions=missions,
                         current_category=category,
                         current_status=status)

@missions_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new mission"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        difficulty = request.form.get('difficulty')
        
        if not all([title, description, category]):
            flash('Please fill in all required fields.', 'error')
            return render_template('missions/create.html')
        
        # Validate difficulty for Help/Favor category
        if category == Mission.CATEGORY_HELP_FAVOR and not difficulty:
            flash('Please select a difficulty level for Help/Favor missions.', 'error')
            return render_template('missions/create.html')
        
        mission = Mission(
            title=title,
            description=description,
            category=category,
            difficulty=difficulty if category == Mission.CATEGORY_HELP_FAVOR else None,
            group_name=current_user.major_group,
            creator_id=current_user.id,
            status=Mission.STATUS_OPEN
        )
        
        # Handle file upload
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
                filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                file.save(filepath)
                mission.attachment_url = f'/static/uploads/{filename}'
        
        db.session.add(mission)
        db.session.commit()
        
        flash('Mission created successfully!', 'success')
        return redirect(url_for('missions.detail', mission_id=mission.id))
    
    return render_template('missions/create.html')

@missions_bp.route('/<int:mission_id>')
def detail(mission_id):
    """Mission detail page"""
    mission = Mission.query.get_or_404(mission_id)
    return render_template('missions/detail.html', mission=mission)

@missions_bp.route('/<int:mission_id>/accept', methods=['POST'])
@login_required
def accept(mission_id):
    """Accept a mission"""
    mission = Mission.query.get_or_404(mission_id)
    
    if mission.status != Mission.STATUS_OPEN:
        flash('This mission is not available.', 'error')
        return redirect(url_for('missions.detail', mission_id=mission_id))
    
    if mission.creator_id == current_user.id:
        flash('You cannot accept your own mission.', 'error')
        return redirect(url_for('missions.detail', mission_id=mission_id))
    
    mission.status = Mission.STATUS_ACCEPTED
    mission.assignee_id = current_user.id
    db.session.commit()
    
    flash('Mission accepted!', 'success')
    return redirect(url_for('missions.detail', mission_id=mission_id))

@missions_bp.route('/<int:mission_id>/complete', methods=['POST'])
@login_required
def complete(mission_id):
    """Complete a mission"""
    mission = Mission.query.get_or_404(mission_id)
    
    if mission.complete(current_user):
        flash(f'Mission completed! You earned {mission.points_awarded} points.', 'success')
    else:
        flash('You cannot complete this mission.', 'error')
    
    return redirect(url_for('missions.detail', mission_id=mission_id))
