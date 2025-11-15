"""
Run script for development server
"""
import os
from backend import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment or default to development
config_name = os.getenv('FLASK_ENV', 'development')

# Create app
app = create_app(config_name)

if __name__ == '__main__':
    # Get host and port from environment or use defaults
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    debug = config_name == 'development'
    
    app.run(host=host, port=port, debug=debug)
