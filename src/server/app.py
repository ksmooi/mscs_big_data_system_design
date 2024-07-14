from flask import Flask, render_template
import psycopg2
import os
import json

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

config = load_config()
db_config = config['data_recorder']['database']

# PostgreSQL connection parameters
DB_HOST = db_config['host']
DB_PORT = db_config['port']
DB_USER = db_config['user']
DB_PASSWORD = db_config['password']
DB_NAME = db_config['dbname']

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
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

        return render_template('index.html', stock_data_results=stock_data_results)

    return app

def run_app():
    app = create_app()
    app.run(host=config['stock_server']['host'], port=config['stock_server']['port'], debug=config['stock_server']['debug'], use_reloader=False)

if __name__ == '__main__':
    run_app()
