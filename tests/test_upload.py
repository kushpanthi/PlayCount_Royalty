import unittest
import io
from backend.app import app

class UploadTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_upload_no_file(self):
        response = self.app.post('/upload')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())
        
    def test_upload_empty_file(self):
        data = {'audio': (io.BytesIO(b''), 'test.wav')}
        response = self.app.post('/upload', data=data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
