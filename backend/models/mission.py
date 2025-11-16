"""
Mission model
"""
from backend import db
from datetime import datetime

class Mission(db.Model):
    """Mission model for tasks students can complete"""
    __tablename__ = 'missions'
    
    # Mission categories
    CATEGORY_HELP_FAVOR = 'Help/Favor'
    CATEGORY_LOST_FOUND = 'Lost & Found'
    CATEGORY_TEAM_STUDY = 'Team/Study Group'
    CATEGORY_EVENT = 'Event'
    
    # Difficulty levels
    DIFFICULTY_EASY = 'Easy'
    DIFFICULTY_MEDIUM = 'Medium'
    DIFFICULTY_HARD = 'Hard'
    
    # Status options
    STATUS_OPEN = 'Open'
    STATUS_ACCEPTED = 'Accepted'
    STATUS_COMPLETED = 'Completed'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=True)  # Only for Help/Favor
    attachment_url = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default=STATUS_OPEN, nullable=False)
    group_name = db.Column(db.String(100), nullable=False)
    
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    points_awarded = db.Column(db.Integer, nullable=True)
    points_invalidated = db.Column(db.Boolean, default=False, nullable=False)
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp(), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    @property
    def points(self):
        """Calculate points based on category and difficulty"""
        from backend.config import Config
        
        if self.category == Mission.CATEGORY_HELP_FAVOR:
            if self.difficulty == Mission.DIFFICULTY_EASY:
                return Config.POINTS_HELP_EASY
            elif self.difficulty == Mission.DIFFICULTY_MEDIUM:
                return Config.POINTS_HELP_MEDIUM
            elif self.difficulty == Mission.DIFFICULTY_HARD:
                return Config.POINTS_HELP_HARD
        elif self.category == Mission.CATEGORY_LOST_FOUND:
            return Config.POINTS_LOST_FOUND
        elif self.category == Mission.CATEGORY_TEAM_STUDY:
            return Config.POINTS_TEAM_STUDY
        elif self.category == Mission.CATEGORY_EVENT:
            return Config.POINTS_EVENT
        return 0
    
    def complete(self, user):
        """Mark mission as completed and award points"""
        if self.status != Mission.STATUS_ACCEPTED:
            return False
        if self.assignee_id != user.id:
            return False
        
        self.status = Mission.STATUS_COMPLETED
        self.completed_at = datetime.utcnow()
        points = self.points
        self.points_awarded = points
        user.points += points
        db.session.commit()
        return True
    
    def invalidate_points(self):
        """Invalidate points for a completed mission"""
        if self.status != Mission.STATUS_COMPLETED or self.points_invalidated:
            return False
        
        if self.assignee and self.points_awarded:
            self.assignee.points -= self.points_awarded
            if self.assignee.points < 0:
                self.assignee.points = 0
        
        self.points_invalidated = True
        db.session.commit()
        return True
    
    def __repr__(self):
        return f'<Mission {self.title}>'
