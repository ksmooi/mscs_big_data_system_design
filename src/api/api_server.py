# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python src/api/api_server.py
# deactivate

from flask import Flask
from api.routes import api_blueprint

def create_app():
    """
    Creates and configures the Flask application.
    
    This function sets up the Flask application and registers the API blueprint
    for handling API routes.
    
    Returns:
        Flask app: Configured Flask application.
    """
    app = Flask(__name__)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    return app

def run_api_server():
    """
    Runs the API Server.
    
    This function creates the Flask application by calling create_app(),
    and then runs the application on the specified host and port.
    """
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)

if __name__ == '__main__':
    """
    Entry point for running the API server directly.
    
    When the script is run directly, this block will execute and start the API server.
    """
    run_api_server()
