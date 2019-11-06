from app import app
import unittest
import base64
import json

class TestLogin(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.user_name = "test2n1@mytest.com"
        self.password = "thi@isMyPass123"
        self.valid_credentials = base64.b64encode(b'test14@mytest.com:P@ssword11').decode('utf-8')
        self.invalid_password = base64.b64encode(b'test@mytest.com:ssword11').decode('utf-8')
        self.invalid_username = base64.b64encode(b'karan@example.com:password11').decode('utf-8')

     def test_user_can_be_retrieved_when_correct_credentials_are_entered(self):
        response = self.app.get(
            '/v1/user/self', headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status, '200 OK')

    def test_user_can_update_with_valid_field(self):
        datajson=json.dumps({"first_name": "Aakawwwwwwsh","last_name": "Jagtap","password": "P@ssword11"})
        response = self.app.put('/v1/user/self',
                                 data=datajson,
                                 content_type='application/json',
                                 headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status_code, 204 )




