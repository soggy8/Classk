"""
User model
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from backend import db

class User(UserMixin, db.Model):
    """User model for students and admins"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    major_group = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, default=0, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    created_missions = db.relationship('Mission', 
                                      foreign_keys='Mission.creator_id',
                                      backref='creator', 
                                      lazy='dynamic',
                                      cascade='all, delete-orphan')
    accepted_missions = db.relationship('Mission',
                                       foreign_keys='Mission.assignee_id',
                                       backref='assignee',
                                       lazy='dynamic')
    
    @property
    def level(self):
        """Calculate user level based on points"""
        from backend.config import Config
        return self.points // Config.POINTS_PER_LEVEL
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'
