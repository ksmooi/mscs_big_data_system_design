# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python data_collector.py
# deactivate

import json
import time
import pika
import yfinance as yf
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os

# Load configuration from JSON file
config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

rabbitmq_config = config['rabbitmq']
data_collector_config = config['data_collector']

# RabbitMQ connection parameters
RABBITMQ_USER = rabbitmq_config['user']
RABBITMQ_PASS = rabbitmq_config['password']
RABBITMQ_HOST = rabbitmq_config['host']
RABBITMQ_PORT = rabbitmq_config['port']
EXCHANGE = 'stockvision_exchange'
EXCHANGE_TYPE = 'topic'
ROUTING_KEY = 'stock.data'
QUEUE = 'stock_data_queue'

# Connection and channel setup
def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    ))

def setup_rabbitmq():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Declare exchange
    channel.exchange_declare(exchange=EXCHANGE, exchange_type=EXCHANGE_TYPE, durable=True)

    # Declare queue
    channel.queue_declare(queue=QUEUE, durable=True)

    # Bind queue to exchange with routing key
    channel.queue_bind(exchange=EXCHANGE, queue=QUEUE, routing_key=ROUTING_KEY)

    connection.close()
    print("RabbitMQ setup completed.")

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")
    if hist.empty:
        print(f"No data found for ticker {ticker}")
        return None
    data = {
        'ticker': ticker,
        'open': float(hist['Open'].iloc[-1]),
        'high': float(hist['High'].iloc[-1]),
        'low': float(hist['Low'].iloc[-1]),
        'close': float(hist['Close'].iloc[-1]),
        'volume': int(hist['Volume'].iloc[-1]),
        'timestamp': datetime.now().isoformat()
    }
    return data

def publish_stock_data(data):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    message = json.dumps(data)
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=ROUTING_KEY,
        body=message
    )
    connection.close()
    #print(f"Published message to {ROUTING_KEY}: {message}")

def collect_and_publish_stock_data():
    for ticker in data_collector_config['stocks']:
        data = fetch_stock_data(ticker)
        if data:  # Ensure data is not None
            #print(f"Received data: {data}")  # Print the data for debugging
            publish_stock_data(data)

def start_producing():
    setup_rabbitmq()
    collect_and_publish_stock_data()
    
    scheduler = BlockingScheduler()
    scheduler.add_job(collect_and_publish_stock_data, 'interval', seconds=data_collector_config['schedule_interval'])
    print(f"Starting data collector with interval {data_collector_config['schedule_interval']} seconds")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Data Collector Service stopped.")

if __name__ == "__main__":
    start_producing()

