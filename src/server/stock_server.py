# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python src/server/stock_server.py
# deactivate

from flask import Flask, render_template
import psycopg2
import os
import json
from datetime import datetime

def load_config():
    """
    Load configuration from a JSON file.
    
    Returns:
        dict: Configuration settings loaded from the JSON file.
    """
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

# Load configuration settings
config = load_config()
db_config = config['data_recorder']['database']

# PostgreSQL connection parameters
DB_HOST = db_config['host']
DB_PORT = db_config['port']
DB_USER = db_config['user']
DB_PASSWORD = db_config['password']
DB_NAME = db_config['dbname']

def get_db_connection():
    """
    Establish and return a connection to the PostgreSQL database.
    
    Returns:
        psycopg2.extensions.connection: A connection object to interact with the PostgreSQL database.
    """
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: The Flask application object.
    """
    app = Flask(__name__)

    @app.route('/')
    def index():
        """
        Render the index page with stock data and server time.
        
        Queries the database for the latest stock data, gets the current server date and time,
        and passes this data to the HTML template for rendering.
        
        Returns:
            str: Rendered HTML page.
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        query_stock_data = """
        SELECT ticker, date, open, high, low, close, volume
        FROM stock_data
        ORDER BY date DESC
        LIMIT 50
        """
        cursor.execute(query_stock_data)
        stock_data_rows = cursor.fetchall()

        cursor.close()
        conn.close()

        stock_data_results = []
        for row in stock_data_rows:
            ticker, date, open, high, low, close, volume = row
            stock_data_results.append({
                'ticker': ticker,
                'date': date,
                'open': open,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })

        # Get current server date and time
        server_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return render_template('index.html', stock_data_results=stock_data_results, server_time=server_time)

    return app

def run_stock_server():
    """
    Run the Flask web server for the StockVision application.
    
    This function creates the Flask app and runs it with the specified host, port, and debug settings.
    """
    app = create_app()
    app.run(host=config['stock_server']['host'], port=config['stock_server']['port'], debug=config['stock_server']['debug'], use_reloader=False)

if __name__ == '__main__':
    """
    Entry point for running the script.
    
    When the script is run directly, this block will execute and start the stock server.
    """
    run_stock_server()
