# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python -m unittest tests/test_api_server.py
# deactivate

import unittest
import json
import sys
import os

# Add the src directory to sys.path to allow importing from src
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from api.api_server import create_app

class APITestCase(unittest.TestCase):
    """
    Test case class for testing the API endpoints of the StockVision project.
    
    This class contains setup for the Flask test client and test methods for each API endpoint.
    """
    
    def setUp(self):
        """
        Sets up the Flask test client and configures the app for testing.
        
        This method is called before each test method.
        """
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_get_stock_data(self):
        """
        Tests the /api/stock_data endpoint.
        
        This test sends a GET request to the /api/stock_data endpoint with a ticker query parameter
        and verifies that the response status code is 200 and the response data is a list of dictionaries
        containing stock data fields.
        """
        response = self.client.get('/api/stock_data?ticker=AAPL')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        if data:
            self.assertIn('ticker', data[0])
            self.assertIn('date', data[0])
            self.assertIn('open', data[0])
            self.assertIn('high', data[0])
            self.assertIn('low', data[0])
            self.assertIn('close', data[0])
            self.assertIn('volume', data[0])

    def test_get_analysis_results(self):
        """
        Tests the /api/analysis_results endpoint.
        
        This test sends a GET request to the /api/analysis_results endpoint with a ticker query parameter
        and verifies that the response status code is 200 and the response data is a list of dictionaries
        containing analysis result fields.
        """
        response = self.client.get('/api/analysis_results?ticker=AAPL')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        if data:
            self.assertIn('ticker', data[0])
            self.assertIn('analysis_date', data[0])
            self.assertIn('ma5', data[0])
            self.assertIn('ma10', data[0])

if __name__ == '__main__':
    """
    Entry point for running the test cases.
    
    When the script is run directly, this block will execute and run all the test cases defined in the class.
    """
    unittest.main()
