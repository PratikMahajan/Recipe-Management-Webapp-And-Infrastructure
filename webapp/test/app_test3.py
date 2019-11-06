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

# Get user information #
    def test_user_can_be_retrieved_when_correct_credentials_are_entered(self):
        response = self.app.get(
            '/v1/user/self', headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status, '200 OK')

#Update user information #
    def test_user_can_update_with_valid_field(self):
        datajson=json.dumps({"first_name": "Aakawwwwwwsh","last_name": "Jagtap","password": "P@ssword11"})
        response = self.app.put('/v1/user/self',
                                 data=datajson,
                                 content_type='application/json',
                                 headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status_code, 204 )

    def test_user_create_recipe_invalid_credentials(self):
        datajson=json.dumps({
            "cook_time_in_min": 15,
            "prep_time_in_min": 15,
            "title": "Creamy Cajun Chicken Pasta",
            "cuisine": "Italian",
            "servings": 2,
            "ingredients": [
                "4 ounces linguine pasta",
                "2 boneless, skinless chicken breast halves, sliced into thin strips",
                "2 teaspoons Cajun seasoning",
                "2 tablespoons butter"
                ],
            "steps": [
                {
                        "position": 1,
                        "items": "some text here"
                }
               ],
            "nutrition_information": {
            "calories": 100,
            "cholesterol_in_mg": 4,
            "sodium_in_mg": 100,
            "carbohydrates_in_grams": 53.7,
            "protein_in_grams": 53.7
            }
        })
        response = self.app.post(
            '/v1/recipe/', data=datajson, content_type='application/json',
                    headers={'Authorization': 'Basic ' + self.valid_credentials})

        self.assertEqual(response.status_code, 201)






