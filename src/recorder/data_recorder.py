# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python src/recorder/data_recorder.py
# deactivate

import json
import pika
import psycopg2
import os
from datetime import datetime

# Load configuration from JSON file
config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

# RabbitMQ configuration parameters
rabbitmq_config = config['rabbitmq']
data_recorder_config = config['data_recorder']

# RabbitMQ connection parameters
RABBITMQ_USER = rabbitmq_config['user']
RABBITMQ_PASS = rabbitmq_config['password']
RABBITMQ_HOST = rabbitmq_config['host']
RABBITMQ_PORT = rabbitmq_config['port']
EXCHANGE = 'stockvision_exchange'
QUEUE = 'stock_data_queue'

# PostgreSQL connection parameters
DB_HOST = data_recorder_config['database']['host']
DB_PORT = data_recorder_config['database']['port']
DB_USER = data_recorder_config['database']['user']
DB_PASSWORD = data_recorder_config['database']['password']
DB_NAME = data_recorder_config['database']['dbname']

def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    
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

def get_rabbitmq_connection():
    """
    Establishes and returns a connection to the RabbitMQ server.
    
    Returns:
        pika.BlockingConnection: A connection object to interact with the RabbitMQ server.
    """
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    ))

def store_stock_data(data):
    """
    Stores stock data into the PostgreSQL database.
    
    Args:
        data (dict): A dictionary containing the stock data to be stored.
    """
    # Print the data for debugging
    # print(f"Storing data: {data}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO stock_data (ticker, date, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (ticker, date) DO UPDATE
    SET open = EXCLUDED.open,
        high = EXCLUDED.high,
        low = EXCLUDED.low,
        close = EXCLUDED.close,
        volume = EXCLUDED.volume;
    """
    try:
        cursor.execute(insert_query, (
            data['ticker'],
            data['date'],
            data.get('open', 0.0),   # Use 0.0 as default value if 'open' key is missing
            data.get('high', 0.0),   # Use 0.0 as default value if 'high' key is missing
            data.get('low', 0.0),    # Use 0.0 as default value if 'low' key is missing
            data.get('close', 0.0),  # Use 0.0 as default value if 'close' key is missing
            data.get('volume', 0)    # Use 0 as default value if 'volume' key is missing
        ))
        conn.commit()
        # Print confirmation for debugging
        # print(f"Stored data for {data['ticker']} on {data['date']}")
    except Exception as e:
        print(f"Error storing data: {e}")
    finally:
        cursor.close()
        conn.close()

def callback(ch, method, properties, body):
    """
    Callback function to process messages from RabbitMQ.
    
    Args:
        ch (BlockingChannel): The channel object.
        method (spec.Basic.Deliver): Method frame with delivery properties.
        properties (spec.BasicProperties): Properties of the message.
        body (bytes): The message body.
    """
    stock_data = json.loads(body)
    # Print the received message for debugging
    # print(f"Received message: {stock_data}")
    
    # Extract the date from the timestamp and prepare the data for storage
    try:
        stock_data['date'] = datetime.fromisoformat(stock_data['timestamp']).date().isoformat()
    except KeyError:
        print("Error: 'timestamp' key not found in the message.")
        return

    store_stock_data(stock_data)

def start_consuming():
    """
    Starts consuming messages from RabbitMQ and processes them using the callback function.
    """
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
    start_consuming()
