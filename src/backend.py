# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python backend.py
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
    start_producing()

# Function to start the Data Recorder Service in a separate thread
def start_data_recorder():
    start_consuming()

# Function to start the Data Analyzer Service in a separate thread
def start_data_analyzer():
    start_analyzing()

# Function to start the Stock Server in a separate thread
def start_stock_server():
    run_stock_server()

# Function to start the API Server in a separate thread
def start_api_server():
    run_api_server()

# Main function to start all services
def main():
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
