import json
import pika
import psycopg2
import os
from datetime import datetime
import pandas as pd

# Load configuration from JSON file
config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

rabbitmq_config = config['rabbitmq']
data_analyzer_config = config['data_analyzer']
db_config = config['data_recorder']['database']

# RabbitMQ connection parameters
RABBITMQ_USER = rabbitmq_config['user']
RABBITMQ_PASS = rabbitmq_config['password']
RABBITMQ_HOST = rabbitmq_config['host']
RABBITMQ_PORT = rabbitmq_config['port']
EXCHANGE = 'stockvision_exchange'
QUEUE = 'stock_data_queue'

# PostgreSQL connection parameters
DB_HOST = db_config['host']
DB_PORT = db_config['port']
DB_USER = db_config['user']
DB_PASSWORD = db_config['password']
DB_NAME = db_config['dbname']

# PostgreSQL connection setup
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

# RabbitMQ connection setup
def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    ))

# Function to perform analysis on stock data
def analyze_stock_data(ticker):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get the last 30 days of stock data
    query = """
    SELECT date, open, high, low, close, volume
    FROM stock_data
    WHERE ticker = %s
    ORDER BY date DESC
    LIMIT 30
    """
    cursor.execute(query, (ticker,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        print(f"No data found for ticker {ticker}")
        return None

    # Convert the data to a DataFrame
    df = pd.DataFrame(rows, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = pd.to_datetime(df['date'])

    # Perform analysis (e.g., calculate moving averages)
    df['ma5'] = df['close'].rolling(window=5).mean()
    df['ma10'] = df['close'].rolling(window=10).mean()

    # Handle NaN values
    ma5 = df['ma5'].iloc[-1]
    ma10 = df['ma10'].iloc[-1]
    if pd.isna(ma5):
        ma5 = None
    if pd.isna(ma10):
        ma10 = None

    # Prepare analysis results
    analysis_result = {
        'ticker': ticker,
        'analysis_date': datetime.now().date().isoformat(),
        'ma5': ma5,
        'ma10': ma10
    }

    return analysis_result

# Function to store analysis results into the PostgreSQL database
def store_analysis_result(result):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO stock_analysis (ticker, analysis_date, analysis_type, result)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        result['ticker'],
        result['analysis_date'],
        'moving_average',
        json.dumps(result)
    ))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Stored analysis result for {result['ticker']} on {result['analysis_date']}")

# Function to process messages from RabbitMQ
def callback(ch, method, properties, body):
    stock_data = json.loads(body)
    ticker = stock_data['ticker']
    print(f"Received message for ticker: {ticker}")

    # Perform analysis
    analysis_result = analyze_stock_data(ticker)
    if analysis_result:
        store_analysis_result(analysis_result)

# Function to start consuming messages from RabbitMQ
def start_analyzing():
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)
    print(f"Waiting for messages from {QUEUE}. To exit press CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()

if __name__ == "__main__":
    start_analyzing()
