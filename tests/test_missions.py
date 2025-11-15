"""
Mission tests
"""
import pytest
from backend import create_app, db
from backend.models.user import User
from backend.models.mission import Mission

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('development')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def user(app):
    """Create a test user"""
    with app.app_context():
        user = User(
            name='Test User',
            email='test@example.com',
            major_group='Computer Science'
        )
        user.set_password('testpass123')
        db.session.add(user)
        db.session.commit()
        return user

def test_create_mission(client, user):
    """Test mission creation"""
    # Login first
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    response = client.post('/missions/create', data={
        'title': 'Test Mission',
        'description': 'Test description',
        'category': 'Help/Favor',
        'difficulty': 'Easy'
    })
    assert response.status_code in [200, 302]

def test_mission_points_calculation():
    """Test mission points calculation"""
    mission = Mission(
        title='Test',
        description='Test',
        category=Mission.CATEGORY_HELP_FAVOR,
        difficulty=Mission.DIFFICULTY_EASY,
        group_name='Computer Science'
    )
    assert mission.points == 20
