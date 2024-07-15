# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python src/backend.py
# deactivate

import threading
import time
from collector.data_collector import start_producing
from recorder.data_recorder import start_consuming
from analyzer.data_analyzer import start_analyzing
from server.stock_server import run_stock_server
from api.api_server import run_api_server
import os
import json

# Load configuration from JSON file
config_path = os.path.join(os.path.dirname(__file__), '../config/config.json')
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

data_collector_config = config['data_collector']

# Function to start the Data Collector Service in a separate thread
def start_data_collector():
    """
    Function to start the Data Collector Service.
    This service fetches stock data from Yahoo Finance API and publishes it to RabbitMQ.
    """
    start_producing()

# Function to start the Data Recorder Service in a separate thread
def start_data_recorder():
    """
    Function to start the Data Recorder Service.
    This service consumes messages from RabbitMQ and stores the collected stock data in the RDBMS.
    """
    start_consuming()

# Function to start the Data Analyzer Service in a separate thread
def start_data_analyzer():
    """
    Function to start the Data Analyzer Service.
    This service analyzes stock data and stores the results in the RDBMS.
    """
    start_analyzing()

# Function to start the Stock Server in a separate thread
def start_stock_server():
    """
    Function to start the Stock Server.
    This server provides a web interface to display analysis results.
    """
    run_stock_server()

# Function to start the API Server in a separate thread
def start_api_server():
    """
    Function to start the API Server.
    This server provides a RESTful API to access stock data and analysis results.
    """
    run_api_server()

# Main function to start all services
def main():
    """
    Main function to start all services of the StockVision Backend Application.
    It starts the Data Collector, Data Recorder, Data Analyzer, Stock Server, and API Server services in separate threads.
    """
    print("Starting StockVision Backend Application")

    # Start Data Collector Service
    data_collector_thread = threading.Thread(target=start_data_collector)
    data_collector_thread.start()
    print("Data Collector Service started")

    # Start Data Recorder Service
    data_recorder_thread = threading.Thread(target=start_data_recorder)
    data_recorder_thread.start()
    print("Data Recorder Service started")

    # Start Data Analyzer Service
    data_analyzer_thread = threading.Thread(target=start_data_analyzer)
    data_analyzer_thread.start()
    print("Data Analyzer Service started")

    # Start Stock Server
    stock_server_thread = threading.Thread(target=start_stock_server)
    stock_server_thread.start()
    print("Stock Server started")

    # Start API Server
    api_server_thread = threading.Thread(target=start_api_server)
    api_server_thread.start()
    print("API Server started")

    # Keep the main thread running to allow other threads to operate
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down StockVision Backend Application")

if __name__ == "__main__":
    main()
