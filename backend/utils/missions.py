"""
Mission utilities
"""
from backend.models.mission import Mission
from backend.config import Config

def calculate_points(category, difficulty=None):
    """Calculate points for a mission based on category and difficulty"""
    if category == Mission.CATEGORY_HELP_FAVOR:
        if difficulty == Mission.DIFFICULTY_EASY:
            return Config.POINTS_HELP_EASY
        elif difficulty == Mission.DIFFICULTY_MEDIUM:
            return Config.POINTS_HELP_MEDIUM
        elif difficulty == Mission.DIFFICULTY_HARD:
            return Config.POINTS_HELP_HARD
    elif category == Mission.CATEGORY_LOST_FOUND:
        return Config.POINTS_LOST_FOUND
    elif category == Mission.CATEGORY_TEAM_STUDY:
        return Config.POINTS_TEAM_STUDY
    elif category == Mission.CATEGORY_EVENT:
        return Config.POINTS_EVENT
    return 0

def get_mission_categories():
    """Get list of mission categories"""
    return [
        Mission.CATEGORY_HELP_FAVOR,
        Mission.CATEGORY_LOST_FOUND,
        Mission.CATEGORY_TEAM_STUDY,
        Mission.CATEGORY_EVENT
    ]

def get_difficulty_levels():
    """Get list of difficulty levels"""
    return [
        Mission.DIFFICULTY_EASY,
        Mission.DIFFICULTY_MEDIUM,
        Mission.DIFFICULTY_HARD
    ]
