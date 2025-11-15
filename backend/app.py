"""
Main application entry point
"""
import os
from backend import create_app

# Get environment or default to development
config_name = os.getenv('FLASK_ENV', 'development')

app = create_app(config_name)

@app.route('/')
def index():
    """Home page route"""
    from flask import render_template
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
