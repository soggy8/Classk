# Classk - Mission-Based Student Engagement Platform

A web application for students to create, accept, and complete missions to earn points and compete on leaderboards within their major/group.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python with Flask
- **Database**: TBD

## Features

### Student Features
- User authentication (sign up/login)
- Create missions
- View mission feed
- Accept and complete missions
- Earn points for completed missions
- View leaderboard
- View profile (points, level, completed missions)

### Admin Features
- View all missions in assigned group
- Invalidate points for completed missions
- Moderate mission content

## Mission System

### Categories
- **Help/Favor**: Easy (20 pts), Medium (40 pts), Hard (60 pts)
- **Lost & Found**: 30 points
- **Team/Study Group**: 20 points
- **Event**: TBD

### Mission Status
- Open
- Accepted
- Completed

## Project Structure

```
Classk/
├── backend/          # Flask application
├── frontend/         # HTML, CSS, JavaScript files
├── static/           # Static assets (images, uploads)
├── templates/        # HTML templates
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.11+
- Conda (or virtual environment)
- PostgreSQL (for shared database) or SQLite (for local development)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/soggy8/Classk.git
   cd Classk
   ```

2. **Create and activate conda environment**
   ```bash
   conda create -n Classk python=3.11
   conda activate Classk
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Set up shared database (for team collaboration)**
   
   **Option A: Use a cloud PostgreSQL database (Recommended)**
   - Sign up for a free PostgreSQL database:
     - [ElephantSQL](https://www.elephantsql.com/) - Free tier: 20MB
     - [Supabase](https://supabase.com/) - Free tier: 500MB
     - [Railway](https://railway.app/) - Free tier available
     - [Neon](https://neon.tech/) - Free tier: 3GB
   - Copy the connection string and add it to `.env`:
     ```
     DATABASE_URL=postgresql://user:password@host:port/database_name
     ```
   - All team members use the same `DATABASE_URL` to share data

   **Option B: Use SQLite (Local only)**
   - Leave `DATABASE_URL` empty in `.env`
   - Database will be created as `classk.db` in the project root
   - Note: This is local only and won't be shared across machines

6. **Run the application**
   ```bash
   conda activate Classk && python run.py
   ```

7. **Access the application**
   - Open browser: http://localhost:5000

### Sharing Data Across Machines

To see each other's accounts and missions:

1. **Use the same PostgreSQL database**
   - One team member creates a PostgreSQL database
   - Shares the `DATABASE_URL` connection string
   - Everyone sets the same `DATABASE_URL` in their `.env` file

2. **Never commit `.env` file**
   - The `.env` file is in `.gitignore`
   - Share connection details securely (not in git)

3. **Initial setup**
   - The first person to run the app will create the database tables
   - Others connecting to the same database will use the same tables

## License

TBD

