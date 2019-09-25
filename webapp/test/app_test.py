from app import app
import unittest
import base64

class TestLogin(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.valid_credentials = base64.b64encode(b'akash@example.com:password11').decode('utf-8')
        self.invalid_password = base64.b64encode(b'akash@example.com:ssword11').decode('utf-8')
        self.invalid_username = base64.b64encode(b'karan@example.com:password11').decode('utf-8')
    
    def test_user_can_be_retrieved_when_correct_credentials_are_entered(self):
        response = self.app.get(
            '/v1/user/self', headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status, '200 OK')


    def test_user_can_be_retrieved_when_invalid_credentials_are_entered(self):
        response = self.app.get(
            '/v1/user/self', headers={'Authorization': 'Basic ' + self.invalid_password})
        self.assertEqual(response.status, '401 UNAUTHORIZED')
