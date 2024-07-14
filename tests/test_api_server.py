# python3 -m venv myenv && source myenv/bin/activate
# pip install --upgrade pip && pip install -r requirements.txt
# python -m unittest discover -s tests
# deactivate

import unittest
import json
import sys
import os

# Add the src directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from api.api_server import create_app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_get_stock_data(self):
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
    unittest.main()
