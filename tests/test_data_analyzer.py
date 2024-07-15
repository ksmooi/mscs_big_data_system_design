# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python -m unittest tests/test_data_analyzer.py
# deactivate

import unittest
from unittest.mock import patch, Mock, MagicMock
import json
import pandas as pd
from datetime import datetime
import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from analyzer.data_analyzer import analyze_stock_data, store_analysis_result, callback

class DataAnalyzerTestCase(unittest.TestCase):
    
    @patch('analyzer.data_analyzer.get_db_connection')
    def test_analyze_stock_data(self, mock_get_db_connection):
        # Mock database connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Sample data returned by the cursor
        sample_data = [
            ('2024-07-01', 100, 110, 90, 105, 1000),
            ('2024-06-30', 102, 112, 92, 108, 1500),
            ('2024-06-29', 104, 114, 94, 110, 1200),
            ('2024-06-28', 106, 116, 96, 112, 1300),
            ('2024-06-27', 108, 118, 98, 114, 1400),
        ]
        mock_cursor.fetchall.return_value = sample_data
        
        result = analyze_stock_data('AAPL')
        
        expected_result = {
            'ticker': 'AAPL',
            'analysis_date': datetime.now().date().isoformat(),
            'ma5': 109.8,  # Calculated moving average
            'ma10': None  # Not enough data for 10-day MA
        }
        
        self.assertEqual(result['ticker'], expected_result['ticker'])
        self.assertEqual(result['analysis_date'], expected_result['analysis_date'])
        self.assertAlmostEqual(result['ma5'], expected_result['ma5'])
        self.assertIsNone(result['ma10'])

    @patch('analyzer.data_analyzer.get_db_connection')
    def test_store_analysis_result(self, mock_get_db_connection):
        # Mock database connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        result = {
            'ticker': 'AAPL',
            'analysis_date': '2024-07-01',
            'ma5': 109.8,
            'ma10': None
        }
        
        store_analysis_result(result)
        
        expected_query = """
    INSERT INTO stock_analysis (ticker, analysis_date, analysis_type, result)
    VALUES (%s, %s, %s, %s)
    """
        mock_cursor.execute.assert_called_once_with(
            expected_query,
            (result['ticker'], result['analysis_date'], 'moving_average', json.dumps(result))
        )
        mock_conn.commit.assert_called_once()

    @patch('analyzer.data_analyzer.analyze_stock_data')
    @patch('analyzer.data_analyzer.store_analysis_result')
    def test_callback(self, mock_store_analysis_result, mock_analyze_stock_data):
        # Sample message
        sample_message = {
            'ticker': 'AAPL',
            'price': 150.00,
            'timestamp': '2024-07-01T12:00:00'
        }
        
        # Mock analysis result
        mock_analysis_result = {
            'ticker': 'AAPL',
            'analysis_date': '2024-07-01',
            'ma5': 109.8,
            'ma10': None
        }
        mock_analyze_stock_data.return_value = mock_analysis_result
        
        # Create a mock channel, method, properties
        mock_channel = Mock()
        mock_method = Mock()
        mock_properties = Mock()
        mock_body = json.dumps(sample_message)
        
        callback(mock_channel, mock_method, mock_properties, mock_body)
        
        mock_analyze_stock_data.assert_called_once_with('AAPL')
        mock_store_analysis_result.assert_called_once_with(mock_analysis_result)

if __name__ == '__main__':
    unittest.main()
