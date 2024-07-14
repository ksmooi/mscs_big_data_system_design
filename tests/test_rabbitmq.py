# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install pika
# pip freeze > requirements.txt
# python test_rabbitmq.py
# deactivate

import pika
import json
import time
import threading

# RabbitMQ connection parameters
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = '24785699'
RABBITMQ_HOST = '192.168.1.150'
RABBITMQ_PORT = 5672

# Connection and channel setup
def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    ))

# Delete existing exchange if exists
def delete_exchange():
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    try:
        channel.exchange_delete(exchange='stockvision_exchange')
        print("Deleted existing exchange 'stockvision_exchange'.")
    except Exception as e:
        print(f"Failed to delete exchange: {e}")
    connection.close()

# Declare exchanges, queues, and bindings
def setup_rabbitmq():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Declare exchange
    channel.exchange_declare(exchange='stockvision_exchange', exchange_type='topic', durable=True)

    # Declare queues
    channel.queue_declare(queue='stock_data_queue', durable=True)
    channel.queue_declare(queue='analysis_results_queue', durable=True)

    # Bind queues to exchange with routing keys
    channel.queue_bind(exchange='stockvision_exchange', queue='stock_data_queue', routing_key='stock.data')
    channel.queue_bind(exchange='stockvision_exchange', queue='analysis_results_queue', routing_key='analysis.results')

    connection.close()
    print("RabbitMQ setup completed.")

# Data Collector Service: Publish stock data
def data_collector_service():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    stock_data = {
        'ticker': 'AAPL',
        'price': 150.00,
        'timestamp': time.time()
    }
    message = json.dumps(stock_data)

    channel.basic_publish(
        exchange='stockvision_exchange',
        routing_key='stock.data',
        body=message
    )
    connection.close()
    print(f"Published message to stock.data: {message}")

# Data Recorder Service: Consume stock data
def data_recorder_service(stop_event):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    def callback(ch, method, properties, body):
        stock_data = json.loads(body)
        print(f"Received message from stock.data: {stock_data}")
        # Simulate recording data to RDBMS
        record_stock_data(stock_data)

    channel.basic_consume(queue='stock_data_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    while not stop_event.is_set():
        connection.process_data_events(time_limit=1)

    channel.stop_consuming()
    connection.close()

def record_stock_data(data):
    # Simulate recording data to a database
    print(f"Recording stock data to RDBMS: {data}")

# Main function
def main():
    delete_exchange()
    setup_rabbitmq()

    # Simulate the Data Collector Service publishing messages
    data_collector_service()

    stop_event = threading.Event()
    recorder_thread = threading.Thread(target=data_recorder_service, args=(stop_event,))
    recorder_thread.start()

    try:
        while recorder_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user. Stopping...")
        stop_event.set()
        recorder_thread.join()

if __name__ == "__main__":
    main()
