# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python src/api/api_server.py
# deactivate

import json
import os
from flask import Flask
from api.routes import api_blueprint

def load_config():
    """
    Loads the configuration from the config.json file.

    Returns:
        dict: Configuration dictionary.
    """
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

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
    config = load_config()
    app = create_app()
    app.run(host=config['api_server']['host'], port=config['api_server']['port'], debug=config['api_server']['debug'], use_reloader=False)

if __name__ == '__main__':
    """
    Entry point for running the API server directly.
    
    When the script is run directly, this block will execute and start the API server.
    """
    run_api_server()
