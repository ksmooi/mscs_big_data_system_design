# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python tests/test_rabbitmq.py
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

def delete_exchange():
    """
    Deletes the existing 'stockvision_exchange' exchange from RabbitMQ if it exists.
    
    This function ensures that any existing exchange is deleted before setting up a new one.
    """
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    try:
        channel.exchange_delete(exchange='stockvision_exchange')
        print("Deleted existing exchange 'stockvision_exchange'.")
    except Exception as e:
        print(f"Failed to delete exchange: {e}")
    connection.close()

def setup_rabbitmq():
    """
    Declares exchanges, queues, and bindings in RabbitMQ.
    
    This function sets up the necessary exchange and queues for the StockVision system,
    and binds the queues to the exchange with specific routing keys.
    """
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

def data_collector_service():
    """
    Publishes stock data to RabbitMQ.
    
    This function simulates the Data Collector Service by publishing a stock data message
    to the 'stockvision_exchange' exchange with the 'stock.data' routing key.
    """
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

def data_recorder_service(stop_event):
    """
    Consumes stock data from RabbitMQ and records it to the RDBMS.
    
    Args:
        stop_event (threading.Event): An event to signal when to stop consuming messages.
    """
    connection = get_rabbitmq_connection()
    channel = connection.channel()

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
        print(f"Received message from stock.data: {stock_data}")
        record_stock_data(stock_data)

    channel.basic_consume(queue='stock_data_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    while not stop_event.is_set():
        connection.process_data_events(time_limit=1)

    channel.stop_consuming()
    connection.close()

def record_stock_data(data):
    """
    Simulates recording stock data to a database.
    
    Args:
        data (dict): A dictionary containing the stock data to be recorded.
    """
    print(f"Recording stock data to RDBMS: {data}")

def main():
    """
    Main function to set up RabbitMQ and run the Data Collector and Data Recorder services.
    
    This function deletes any existing exchange, sets up the necessary RabbitMQ components,
    starts the Data Collector Service, and runs the Data Recorder Service in a separate thread.
    """
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
    """
    Entry point for running the script.
    
    When the script is run directly, this block will execute and start the main function.
    """
    main()
