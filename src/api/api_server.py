from flask import Flask
from api.routes import api_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    return app

def run_app():
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_app()
