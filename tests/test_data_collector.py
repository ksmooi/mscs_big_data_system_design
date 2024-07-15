# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python -m unittest tests/test_data_collector.py
# deactivate

import unittest
import json
import sys
import os
import pandas as pd
from datetime import datetime
from unittest.mock import patch, Mock

# Add the src directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from collector.data_collector import setup_rabbitmq, fetch_stock_data, publish_stock_data, collect_and_publish_stock_data

class DataCollectorTestCase(unittest.TestCase):
    
    @patch('collector.data_collector.get_rabbitmq_connection')
    def test_setup_rabbitmq(self, mock_get_rabbitmq_connection):
        mock_conn = Mock()
        mock_channel = Mock()
        mock_get_rabbitmq_connection.return_value = mock_conn
        mock_conn.channel.return_value = mock_channel

        setup_rabbitmq()

        mock_channel.exchange_declare.assert_called_once_with(exchange='stockvision_exchange', exchange_type='topic', durable=True)
        mock_channel.queue_declare.assert_called_once_with(queue='stock_data_queue', durable=True)
        mock_channel.queue_bind.assert_called_once_with(exchange='stockvision_exchange', queue='stock_data_queue', routing_key='stock.data')
        mock_conn.close.assert_called_once()

    @patch('collector.data_collector.yf.Ticker')
    def test_fetch_stock_data(self, mock_yf_ticker):
        mock_ticker = Mock()
        mock_yf_ticker.return_value = mock_ticker
        sample_hist = pd.DataFrame({
            'Open': [100.0],
            'High': [110.0],
            'Low': [90.0],
            'Close': [105.0],
            'Volume': [1000]
        }, index=[datetime.now()])
        mock_ticker.history.return_value = sample_hist

        result = fetch_stock_data('AAPL')

        expected_result = {
            'ticker': 'AAPL',
            'open': 100.0,
            'high': 110.0,
            'low': 90.0,
            'close': 105.0,
            'volume': 1000,
            'timestamp': datetime.now().isoformat()
        }

        self.assertEqual(result['ticker'], expected_result['ticker'])
        self.assertEqual(result['open'], expected_result['open'])
        self.assertEqual(result['high'], expected_result['high'])
        self.assertEqual(result['low'], expected_result['low'])
        self.assertEqual(result['close'], expected_result['close'])
        self.assertEqual(result['volume'], expected_result['volume'])
        self.assertEqual(result['timestamp'][:19], expected_result['timestamp'][:19])  # Compare up to seconds

    @patch('collector.data_collector.get_rabbitmq_connection')
    def test_publish_stock_data(self, mock_get_rabbitmq_connection):
        mock_conn = Mock()
        mock_channel = Mock()
        mock_get_rabbitmq_connection.return_value = mock_conn
        mock_conn.channel.return_value = mock_channel

        data = {
            'ticker': 'AAPL',
            'open': 100.0,
            'high': 110.0,
            'low': 90.0,
            'close': 105.0,
            'volume': 1000,
            'timestamp': datetime.now().isoformat()
        }

        publish_stock_data(data)

        message = json.dumps(data)
        mock_channel.basic_publish.assert_called_once_with(
            exchange='stockvision_exchange',
            routing_key='stock.data',
            body=message
        )
        mock_conn.close.assert_called_once()

    @patch('collector.data_collector.fetch_stock_data')
    @patch('collector.data_collector.publish_stock_data')
    def test_collect_and_publish_stock_data(self, mock_publish_stock_data, mock_fetch_stock_data):
        mock_fetch_stock_data.return_value = {
            'ticker': 'AAPL',
            'open': 100.0,
            'high': 110.0,
            'low': 90.0,
            'close': 105.0,
            'volume': 1000,
            'timestamp': datetime.now().isoformat()
        }

        collect_and_publish_stock_data()

        self.assertTrue(mock_fetch_stock_data.called)
        self.assertTrue(mock_publish_stock_data.called)

if __name__ == '__main__':
    unittest.main()
