"""
Authentication utilities
"""

def is_admin(user):
    """Check if user is an admin"""
    return user.is_authenticated and user.is_admin

def can_accept_mission(user, mission):
    """Check if user can accept a mission"""
    if not user.is_authenticated:
        return False
    if mission.creator_id == user.id:
        return False
    if mission.status != 'Open':
        return False
    return True

def can_complete_mission(user, mission):
    """Check if user can complete a mission"""
    if not user.is_authenticated:
        return False
    if mission.assignee_id != user.id:
        return False
    if mission.status != 'Accepted':
        return False
    return True
