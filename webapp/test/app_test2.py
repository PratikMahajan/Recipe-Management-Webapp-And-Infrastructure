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
        self.valid_credentials = base64.b64encode(b'pratik@mahajan.xyz:123@Abcd').decode('utf-8')
        self.invalid_password = base64.b64encode(b'test@mytest.com:ssword11').decode('utf-8')
        self.invalid_username = base64.b64encode(b'karan@example.com:password11').decode('utf-8')

    def test_user_create_recipe(self):
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

    def test_user_recipe_get(self):
        response = self.app.get(
            '/v1/recipe/f5e02bd4-55da-4243-b7fb-980b230a1138')
        self.assertEqual(response.status_code, 404)

    def test_user_recipe_delete(self):
        response = self.app.delete(
            '/v1/recipe/f5e02bd4-55da-4243-b7fb-980b230a1138', headers={'Authorization': 'Basic ' + self.valid_credentials})
        self.assertEqual(response.status_code, 403)




