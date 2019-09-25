from app import app
import unittest
import base64
import json

class TestLogin(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.user_name = "test12@mytest.com"
        self.password = "thi@isMyPass123"
        self.valid_credentials = base64.b64encode(b'test@mytest.com:thi@isMyPass123').decode('utf-8')
        self.invalid_password = base64.b64encode(b'test@mytest.com:ssword11').decode('utf-8')
        self.invalid_username = base64.b64encode(b'karan@example.com:password11').decode('utf-8')

    def test_user_create_account(self):
        response = self.app.post(
            '/v1/user', data=json.dumps({
                    "email_address":self.user_name,
                    "password":self.password,
                    "first_name":"TestUser",
                    "last_name":"lastName"
                    }), content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)


    def test_user_can_be_retrieved_when_correct_credentials_are_entered(self):
        response = self.app.get(
            '/v1/user/self', headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status, '200 OK')


    def test_user_can_be_retrieved_when_invalid_credentials_are_entered(self):
        response = self.app.get(
            '/v1/user/self', headers={'Authorization': 'Basic ' + self.invalid_password})
        self.assertEqual(response.status, '401 UNAUTHORIZED')

