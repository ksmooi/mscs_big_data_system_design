from flask import Blueprint, jsonify, request
import psycopg2
import os
import json

api_blueprint = Blueprint('api', __name__)

# Load configuration from JSON file
config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

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

@api_blueprint.route('/stock_data', methods=['GET'])
def get_stock_data():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT ticker, date, open, high, low, close, volume
    FROM stock_data
    WHERE ticker = %s
    ORDER BY date DESC
    LIMIT 50
    """
    cursor.execute(query, (ticker,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    stock_data = []
    for row in rows:
        ticker, date, open, high, low, close, volume = row
        stock_data.append({
            'ticker': ticker,
            'date': date,
            'open': open,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })

    return jsonify(stock_data)

@api_blueprint.route('/analysis_results', methods=['GET'])
def get_analysis_results():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({'error': 'Ticker is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT ticker, analysis_date, result
    FROM stock_analysis
    WHERE ticker = %s AND analysis_type = 'moving_average'
    ORDER BY analysis_date DESC
    LIMIT 50
    """
    cursor.execute(query, (ticker,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    analysis_results = []
    for row in rows:
        ticker, analysis_date, result = row
        if isinstance(result, str):
            result_json = json.loads(result)
        else:
            result_json = result
        analysis_results.append({
            'ticker': ticker,
            'analysis_date': analysis_date,
            'ma5': result_json['ma5'],
            'ma10': result_json['ma10']
        })

    return jsonify(analysis_results)
