"""
Mission routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload
import os
from backend import db
from backend.models.mission import Mission
from backend.models.user import User
from backend.models.rating import Rating
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
        # Show all missions to authenticated users (from all groups)
        query = Mission.query.options(joinedload(Mission.creator))
    else:
        # For non-authenticated users, show no missions
        query = Mission.query.filter(False)
    
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
    # Load mission with creator relationship
    mission = Mission.query.options(
        joinedload(Mission.creator)
    ).get_or_404(mission_id)
    
    # Load ratings for Event missions
    ratings = []
    average_rating = None
    user_rating = None
    
    if mission.category == Mission.CATEGORY_EVENT:
        ratings = Rating.query.options(
            joinedload(Rating.user)
        ).filter_by(mission_id=mission_id).order_by(Rating.created_at.desc()).all()
        
        if ratings:
            average_rating = sum(r.rating for r in ratings) / len(ratings)
        
        # Check if current user has rated
        if current_user.is_authenticated:
            user_rating = Rating.query.filter_by(
                mission_id=mission_id,
                user_id=current_user.id
            ).first()
    
    return render_template('missions/detail.html', 
                         mission=mission,
                         ratings=ratings,
                         average_rating=average_rating,
                         user_rating=user_rating)

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
        if mission.category == Mission.CATEGORY_EVENT:
            flash(f'Event completed! You earned {mission.points_awarded} points. You can now rate this event below.', 'success')
        else:
            flash(f'Mission completed! You earned {mission.points_awarded} points.', 'success')
    else:
        flash('You cannot complete this mission.', 'error')
    
    return redirect(url_for('missions.detail', mission_id=mission_id))

@missions_bp.route('/<int:mission_id>/rate', methods=['POST'])
@login_required
def rate_event(mission_id):
    """Rate an Event mission"""
    mission = Mission.query.get_or_404(mission_id)
    
    # Only allow rating Event missions
    if mission.category != Mission.CATEGORY_EVENT:
        flash('Only Event missions can be rated.', 'error')
        return redirect(url_for('missions.detail', mission_id=mission_id))
    
    # User must have completed the mission to rate it
    if mission.status != Mission.STATUS_COMPLETED or mission.assignee_id != current_user.id:
        flash('You can only rate events you have completed.', 'error')
        return redirect(url_for('missions.detail', mission_id=mission_id))
    
    rating_value = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()
    
    if not rating_value or rating_value < 1 or rating_value > 5:
        flash('Please provide a valid rating (1-5 stars).', 'error')
        return redirect(url_for('missions.detail', mission_id=mission_id))
    
    # Check if user has already rated
    existing_rating = Rating.query.filter_by(
        mission_id=mission_id,
        user_id=current_user.id
    ).first()
    
    if existing_rating:
        # Update existing rating
        existing_rating.rating = rating_value
        existing_rating.comment = comment
        flash('Rating updated successfully!', 'success')
    else:
        # Create new rating
        rating = Rating(
            mission_id=mission_id,
            user_id=current_user.id,
            rating=rating_value,
            comment=comment
        )
        db.session.add(rating)
        flash('Thank you for rating this event!', 'success')
    
    db.session.commit()
    return redirect(url_for('missions.detail', mission_id=mission_id))
