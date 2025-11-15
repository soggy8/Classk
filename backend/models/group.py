"""
Group/Major model
"""
from backend import db

class Group(db.Model):
    """Group/Major model for organizing users and missions"""
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    admin = db.relationship('User', foreign_keys=[admin_id], backref='admin_groups')
    users = db.relationship('User', 
                           primaryjoin='User.major_group == Group.name',
                           foreign_keys='User.major_group',
                           viewonly=True)
    missions = db.relationship('Mission',
                              primaryjoin='Mission.group_name == Group.name',
                              foreign_keys='Mission.group_name',
                              viewonly=True)
    
    def __repr__(self):
        return f'<Group {self.name}>'
