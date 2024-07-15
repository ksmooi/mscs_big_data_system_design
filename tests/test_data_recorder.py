# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python -m unittest tests/test_data_recorder.py
# deactivate

import unittest
from unittest.mock import patch, Mock
import json
from datetime import datetime
import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from recorder.data_recorder import get_db_connection, get_rabbitmq_connection, store_stock_data, callback, start_consuming

class DataRecorderTestCase(unittest.TestCase):
    
    @patch('recorder.data_recorder.psycopg2.connect')
    def test_get_db_connection(self, mock_connect):
        get_db_connection()
        mock_connect.assert_called_once_with(
            host='localhost',
            port=5432,
            user='mscs_dba',
            password='24785699',
            dbname='stock_vision_db'
        )

    @patch('recorder.data_recorder.pika.BlockingConnection')
    def test_get_rabbitmq_connection(self, mock_blocking_connection):
        get_rabbitmq_connection()
        mock_blocking_connection.assert_called_once()

    @patch('recorder.data_recorder.get_db_connection')
    def test_store_stock_data(self, mock_get_db_connection):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        data = {
            'ticker': 'AAPL',
            'date': '2024-07-01',
            'open': 100.0,
            'high': 110.0,
            'low': 90.0,
            'close': 105.0,
            'volume': 1000
        }

        store_stock_data(data)

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
        mock_cursor.execute.assert_called_once_with(insert_query, (
            data['ticker'],
            data['date'],
            data.get('open', 0.0),
            data.get('high', 0.0),
            data.get('low', 0.0),
            data.get('close', 0.0),
            data.get('volume', 0)
        ))
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('recorder.data_recorder.store_stock_data')
    def test_callback(self, mock_store_stock_data):
        body = {
            'ticker': 'AAPL',
            'timestamp': '2024-07-01T00:00:00'
        }
        body_bytes = json.dumps(body).encode('utf-8')

        mock_channel = Mock()
        mock_method = Mock()
        mock_properties = Mock()

        callback(mock_channel, mock_method, mock_properties, body_bytes)

        expected_data = {
            'ticker': 'AAPL',
            'timestamp': '2024-07-01T00:00:00',
            'date': '2024-07-01'
        }

        mock_store_stock_data.assert_called_once_with(expected_data)

    @patch('recorder.data_recorder.get_rabbitmq_connection')
    @patch('recorder.data_recorder.callback')
    def test_start_consuming(self, mock_callback, mock_get_rabbitmq_connection):
        mock_conn = Mock()
        mock_channel = Mock()
        mock_get_rabbitmq_connection.return_value = mock_conn
        mock_conn.channel.return_value = mock_channel

        def stop_consuming():
            mock_channel.stop_consuming()

        mock_channel.start_consuming.side_effect = stop_consuming

        start_consuming()

        mock_channel.queue_declare.assert_called_once_with(queue='stock_data_queue', durable=True)
        mock_channel.basic_consume.assert_called_once_with(queue='stock_data_queue', on_message_callback=mock_callback, auto_ack=True)
        mock_channel.start_consuming.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
