"""
Authentication routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from backend import db
from backend.models.user import User
from backend.models.group import Group

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please provide both email and password.', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        major_group = request.form.get('major_group')
        
        # Validation
        if not all([name, email, password, major_group]):
            flash('Please fill in all fields.', 'error')
            return render_template('auth/signup.html')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('auth/signup.html')
        
        # Create new user
        user = User(
            name=name,
            email=email,
            major_group=major_group,
            points=0
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Create group if it doesn't exist
        group = Group.query.filter_by(name=major_group).first()
        if not group:
            group = Group(name=major_group)
            db.session.add(group)
            db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    # Get available groups for dropdown
    groups = Group.query.all()
    return render_template('auth/signup.html', groups=groups)

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
