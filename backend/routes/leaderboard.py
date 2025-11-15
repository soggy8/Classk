"""
Leaderboard routes
"""
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from backend import db
from backend.models.user import User
from backend.models.mission import Mission
from sqlalchemy import func, case

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/')
@login_required
def index():
    """Leaderboard page showing top users by different criteria"""
    leaderboard_type = request.args.get('type', 'overall')  # overall, help_favor, lost_found, team_study, event
    scope = request.args.get('scope', 'group')  # group or global
    
    # Base query - filter by scope
    if scope == 'group':
        base_query = User.query.filter_by(major_group=current_user.major_group)
    else:
        base_query = User.query
    
    top_users = []
    user_rank = None
    user_points = 0
    
    if leaderboard_type == 'overall':
        # Most points overall
        top_users = base_query.order_by(User.points.desc()).limit(10).all()
        
        # Get user's rank
        if scope == 'group':
            user_rank = User.query.filter(
                User.major_group == current_user.major_group,
                User.points > current_user.points
            ).count() + 1
        else:
            user_rank = User.query.filter(User.points > current_user.points).count() + 1
        
        user_points = current_user.points
        
    else:
        # Category-specific leaderboards
        category_map = {
            'help_favor': Mission.CATEGORY_HELP_FAVOR,
            'lost_found': Mission.CATEGORY_LOST_FOUND,
            'team_study': Mission.CATEGORY_TEAM_STUDY,
            'event': Mission.CATEGORY_EVENT
        }
        
        category = category_map.get(leaderboard_type, Mission.CATEGORY_HELP_FAVOR)
        
        # Calculate points per user from completed missions in this category
        # Only count non-invalidated points
        query = db.session.query(
            User.id,
            User.name,
            User.email,
            User.major_group,
            func.sum(
                case(
                    (Mission.points_invalidated == False, Mission.points_awarded),
                    else_=0
                )
            ).label('category_points')
        ).select_from(User).join(
            Mission, 
            User.id == Mission.assignee_id
        ).filter(
            Mission.status == Mission.STATUS_COMPLETED,
            Mission.category == category
        )
        
        if scope == 'group':
            query = query.filter(User.major_group == current_user.major_group)
        
        query = query.group_by(User.id, User.name, User.email, User.major_group)\
                     .order_by(func.sum(
                         case(
                             (Mission.points_invalidated == False, Mission.points_awarded),
                             else_=0
                         )
                     ).desc())\
                     .limit(10)
        
        results = query.all()
        
        # Convert results to user-like objects with category_points
        class CategoryLeaderboardEntry:
            def __init__(self, user_id, name, email, major_group, category_points):
                self.id = user_id
                self.name = name
                self.email = email
                self.major_group = major_group
                self.points = int(category_points or 0)
                self.category_points = int(category_points or 0)
            
            @property
            def level(self):
                """Calculate level from category points (for consistency)"""
                from backend.config import Config
                return self.points // Config.POINTS_PER_LEVEL
        
        top_users = [
            CategoryLeaderboardEntry(r.id, r.name, r.email, r.major_group, r.category_points)
            for r in results
        ]
        
        # Get user's category points
        user_category_query = db.session.query(
            func.sum(
                case(
                    (Mission.points_invalidated == False, Mission.points_awarded),
                    else_=0
                )
            ).label('category_points')
        ).select_from(Mission).filter(
            Mission.assignee_id == current_user.id,
            Mission.status == Mission.STATUS_COMPLETED,
            Mission.category == category
        )
        
        if scope == 'group':
            user_category_query = user_category_query.join(
                User, Mission.assignee_id == User.id
            ).filter(User.major_group == current_user.major_group)
        
        user_category_result = user_category_query.scalar()
        user_points = int(user_category_result or 0)
        
        # Get user's rank in category
        rank_subquery = db.session.query(
            Mission.assignee_id,
            func.sum(
                case(
                    (Mission.points_invalidated == False, Mission.points_awarded),
                    else_=0
                )
            ).label('category_points')
        ).filter(
            Mission.status == Mission.STATUS_COMPLETED,
            Mission.category == category
        )
        
        if scope == 'group':
            rank_subquery = rank_subquery.join(
                User, Mission.assignee_id == User.id
            ).filter(User.major_group == current_user.major_group)
        
        rank_subquery = rank_subquery.group_by(Mission.assignee_id)\
                                     .having(func.sum(
                                         case(
                                             (Mission.points_invalidated == False, Mission.points_awarded),
                                             else_=0
                                         )
                                     ) > user_points)\
                                     .subquery()
        
        user_rank = db.session.query(func.count()).select_from(rank_subquery).scalar() + 1
    
    # Get category display name
    category_names = {
        'overall': 'Most Points Overall',
        'help_favor': 'Help/Favor',
        'lost_found': 'Lost & Found',
        'team_study': 'Team/Study Group',
        'event': 'Event'
    }
    
    category_name = category_names.get(leaderboard_type, 'Overall')
    
    return render_template('leaderboard/index.html',
                         top_users=top_users,
                         current_user=current_user,
                         user_rank=user_rank,
                         user_points=user_points,
                         leaderboard_type=leaderboard_type,
                         category_name=category_name,
                         scope=scope)
