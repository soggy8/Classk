"""
Event Rating model
"""
from backend import db
from datetime import datetime

class Rating(db.Model):
    """Rating model for Event missions"""
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('missions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    
    # Relationships
    mission = db.relationship('Mission', backref='ratings')
    user = db.relationship('User', backref='ratings')
    
    # Ensure one rating per user per mission
    __table_args__ = (db.UniqueConstraint('mission_id', 'user_id', name='unique_user_mission_rating'),)
    
    @property
    def stars(self):
        """Return star representation"""
        return '⭐' * self.rating
    
    def __repr__(self):
        return f'<Rating {self.rating} stars for Mission {self.mission_id} by User {self.user_id}>'

