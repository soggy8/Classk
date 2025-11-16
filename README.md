# Classk - Mission-Based Student Engagement Platform

A web application for students to create, accept, and complete missions to earn points and compete on leaderboards within their major/group.

## 🚀 Features

### Student Features
- ✅ User authentication (sign up/login/logout)
- ✅ Create missions with categories, difficulty levels, and file attachments
- ✅ View mission feed (all missions from all groups)
- ✅ Accept and complete missions
- ✅ Earn points for completed missions
- ✅ View leaderboards (overall and category-specific, group and global)
- ✅ View profile with stats, level, and mission history
- ✅ Rate Event missions (1-5 stars with comments)

### Admin Features
- ✅ View all missions in assigned group
- ✅ Filter missions by category, status, and creator
- ✅ Invalidate points for completed missions
- ✅ Admin dashboard with statistics

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS (with glassmorphism design), JavaScript
- **Backend**: Python 3.x with Flask
- **Database**: SQLite (default) - can be configured for PostgreSQL
- **Authentication**: Flask-Login with password hashing
- **Styling**: Custom design system with gradients, animations, and Poppins font

## 📋 Mission System

### Categories
- **Help/Favor**: Easy (20 pts), Medium (40 pts), Hard (60 pts)
- **Lost & Found**: 30 points
- **Team/Study Group**: 20 points
- **Event**: 25 points (with rating system)

### Mission Status
- **Open**: Available for acceptance
- **Accepted**: Assigned to a user
- **Completed**: Finished by assignee

### Points & Levels
- Points are awarded based on category and difficulty
- Level = Points ÷ 100 (every 100 points = 1 level)

## 📁 Project Structure

```
Classk/
├── backend/              # Flask application
│   ├── __init__.py      # App factory
│   ├── config.py        # Configuration
│   ├── models/          # Database models (User, Mission, Group, Rating)
│   ├── routes/          # Route blueprints (auth, missions, profile, leaderboard, admin)
│   └── utils/           # Utility functions
├── frontend/            # Static files (served as Flask static folder)
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── images/         # Images (logo, etc.)
├── static/             # Additional static assets
│   ├── images/         # Logo files
│   └── uploads/        # Mission attachments
├── templates/          # Jinja2 HTML templates
│   ├── auth/          # Login and signup
│   ├── missions/      # Mission pages
│   ├── admin/         # Admin dashboard
│   └── ...
├── tests/             # Test files
├── run.py             # Development server entry point
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## 🏃 Getting Started

### Prerequisites

- Python 3.8+
- Conda (recommended) or pip
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Classk
   ```

2. **Create a Conda environment (recommended)**
   ```bash
   conda create -n classk python=3.10
   conda activate classk
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables (optional)**
   ```bash
   # Create a .env file in the project root
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=development
   DATABASE_URL=sqlite:///classk.db  # Optional, defaults to SQLite
   ```

5. **Run the application**
   ```bash
   python run.py
   ```
   
   Or:
   ```bash
   flask --app backend.app run
   ```

   The application will be available at `http://localhost:5000`

### Database

The database is automatically created on first run using SQLite. The database file `classk.db` will be created in the project root.

**To reset the database:**
```bash
# Delete the database file
rm classk.db

# Restart the application - it will create a new database
python run.py
```

## 👤 Admin Access

To access the admin dashboard, you need to set your user account as an admin:

1. **Using Python:**
   ```python
   from backend import create_app, db
   from backend.models.user import User
   
   app = create_app()
   with app.app_context():
       user = User.query.filter_by(email='your-email@example.com').first()
       user.is_admin = True
       db.session.commit()
   ```

2. **Using SQLite:**
   ```bash
   sqlite3 classk.db
   UPDATE users SET is_admin = 1 WHERE email = 'your-email@example.com';
   ```

After setting admin status, log out and log back in to see the "Admin" link in the navbar.

## 🎨 Design System

The application uses a custom design system:
- **Colors**: Purple (#A855FF) and Pink (#EC4899) gradients
- **Typography**: Poppins font family
- **Effects**: Glassmorphism (frosted glass) with backdrop blur
- **Animations**: Entrance animations with staggered delays
- **Layout**: Responsive, mobile-first design

## 🔧 Configuration

Key configuration options in `backend/config.py`:
- `SECRET_KEY`: Flask secret key (set via environment variable)
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `POINTS_HELP_EASY/MEDIUM/HARD`: Points for Help/Favor missions
- `POINTS_LOST_FOUND`: Points for Lost & Found missions
- `POINTS_TEAM_STUDY`: Points for Team/Study Group missions
- `POINTS_EVENT`: Points for Event missions
- `POINTS_PER_LEVEL`: Points required per level (default: 100)
- `AVAILABLE_MAJORS`: List of predefined majors for signup

## 📝 Available Majors

Users can select from these majors when signing up:
- Computer Science
- Engineering
- Business Administration
- Medicine
- Law
- Arts & Humanities
- Science
- Education
- Psychology
- Social Sciences
- Mathematics
- Physics
- Chemistry
- Biology
- Economics
- Communications
- Architecture
- Other

## 🚀 Development

### Running in Development Mode

```bash
python run.py
```

The app runs with debug mode enabled by default in development.

### Project Structure Notes

- **Flask App Factory Pattern**: Application is created in `backend/__init__.py`
- **Blueprints**: Routes are organized into separate blueprint files
- **Models**: SQLAlchemy models for User, Mission, Group, and Rating
- **Static Files**: Served from `frontend/` directory
- **Templates**: Jinja2 templates with base template and blocks

## 📚 Routes

### Authentication
- `GET/POST /auth/login` - User login
- `GET/POST /auth/signup` - User registration
- `GET /auth/logout` - User logout

### Missions
- `GET /missions/` - List all missions (with filters)
- `GET /missions/create` - Create mission form
- `POST /missions/create` - Submit mission
- `GET /missions/<id>` - Mission detail
- `POST /missions/<id>/accept` - Accept mission
- `POST /missions/<id>/complete` - Complete mission
- `POST /missions/<id>/rate` - Rate Event mission (Event only)

### Profile
- `GET /profile/` - User profile page

### Leaderboard
- `GET /leaderboard/` - View leaderboards (overall or category-specific, group or global)

### Admin
- `GET /admin/dashboard` - Admin dashboard (admin only)
- `POST /admin/invalidate/<id>` - Invalidate mission points (admin only)

### Home
- `GET /` - Home page

## 🔐 Security Notes

- Passwords are hashed using Werkzeug
- Admin routes are protected with `@admin_required` decorator
- File uploads are restricted by extension and size (16MB max)
- Secret key should be set via environment variable in production

## 📄 License

TBD

## 👥 Contributing

This is a student project. For contributions, please coordinate with the team.

## 🐛 Known Issues / Future Improvements

Key areas for enhancement:
- CSRF protection (Flask-WTF installed but not configured)
- Password reset functionality
- Enhanced input validation
- Database migrations (Flask-Migrate)
- Logging system
- Unit tests
- Production deployment configuration
