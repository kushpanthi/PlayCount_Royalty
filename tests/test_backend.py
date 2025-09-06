import unittest
import os
import tempfile
from backend.app import app, allowed_file
from backend.dejavu_setup import get_dejavu_config

class BasicTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.get_json())
        
    def test_allowed_file(self):
        self.assertTrue(allowed_file('test.wav'))
        self.assertTrue(allowed_file('test.mp3'))
        self.assertFalse(allowed_file('test.txt'))
        self.assertFalse(allowed_file('test.exe'))
        
    def test_dejavu_config(self):
        config = get_dejavu_config()
        self.assertIn('database', config)
        self.assertIn('database_type', config)

if __name__ == '__main__':
    unittest.main()
