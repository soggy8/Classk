"""
Authentication tests
"""
import pytest
from backend import create_app, db
from backend.models.user import User

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

def test_user_registration(client):
    """Test user registration"""
    response = client.post('/auth/signup', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'testpass123',
        'major_group': 'Computer Science'
    })
    assert response.status_code in [200, 302]  # May redirect

def test_user_login(client):
    """Test user login"""
    # First create a user
    with client.application.app_context():
        user = User(
            name='Test User',
            email='test@example.com',
            major_group='Computer Science'
        )
        user.set_password('testpass123')
        db.session.add(user)
        db.session.commit()
    
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    assert response.status_code in [200, 302]
