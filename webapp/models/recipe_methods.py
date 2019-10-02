import uuid
from flask import Response, jsonify
from datetime import datetime
from config.loggingfilter import *
from config.logger import *
import json
from models.recipe import *
from models.ingredients import *
from models.nutritioninformation import *
from models.steps import *

def round_to_5(number):
    try:
        return int(math.ceil(number / 5.0)) * 5
    except:
        raise ValueError('Incorrect Time Format')


def insert_recipe(cursor, recipeJson, authorID, recipeID = None, createdTime = None):
    try:
        id = str(uuid.uuid4())
        if recipeID:
            id = recipeID
        cook_time_in_min = recipeJson['cook_time_in_min']
        prep_time_in_min = recipeJson['prep_time_in_min']

        if cook_time_in_min % 5 != 0:
            raise ValueError('Incorrect Cook Time')
        if prep_time_in_min % 5 != 0:
            raise ValueError('Incorrect Prep Time')

        total_time_in_min = cook_time_in_min + prep_time_in_min
        title = recipeJson["title"]
        cuisine = recipeJson["cuisine"]
        servings = recipeJson["servings"]
        author_id = authorID
        created_ts = createdTime
        if not createdTime:
            created_ts = str(datetime.now())
        updated_ts = str(datetime.now())

        if servings > 5 or servings < 1:
            raise ValueError('Incorrect Servings')

        recipe = Recipe(id = id , cook_time_in_min=cook_time_in_min, prep_time_in_min=prep_time_in_min,
                        total_time_in_min=total_time_in_min, title=title, cuisine=cuisine, servings=servings,
                        author_id=author_id, created_ts=created_ts, updated_ts=updated_ts)

        nutrition = recipeJson["nutrition_information"]
        recipe_id = id
        calories = float(nutrition["calories"])
        cholesterol_in_mg = nutrition["cholesterol_in_mg"]
        sodium_in_mg = nutrition["sodium_in_mg"]
        carbohydrates_in_grams = float(nutrition["carbohydrates_in_grams"])
        protein_in_grams = float(nutrition["protein_in_grams"])

        nutritioninformation = NutritionInformation(recipe_id=recipe_id, calories=calories,
                                                    cholesterol_in_mg=cholesterol_in_mg, sodium_in_mg=sodium_in_mg,
                                                    carbohydrates_in_grams=carbohydrates_in_grams,
                                                    protein_in_grams=protein_in_grams)

        ingredientset = set(recipeJson["ingredients"])
        for ingred in ingredientset:
            newIngred = Ingredients(recipe_id=recipe_id, ingredient=ingred)
            cursor.add(newIngred)

        steps = recipeJson["steps"]
        for step in steps:
            position = step['position']
            items = step['items']
            if position < 1:
                raise ValueError('Error in Positions')
            insertStep = Steps(recipe_id=recipe_id, position=position, items=items)
            cursor.add(insertStep)


        cursor.add(recipe)
        cursor.add(nutritioninformation)
        cursor.commit()
        recipeJson["id"]=id
        recipeJson["created_ts"]=created_ts
        recipeJson["updated_ts"]=updated_ts
        recipeJson["total_time_in_min"]=total_time_in_min
        recipeJson["author_id"]=authorID
        return jsonify(recipeJson), 201 

    except Exception as e:
        cursor.rollback()
        logger.debug("Exception in creating recipe: "+str(e))
        raise Exception(str(e))


def get_recipy(cursor, recipe_id):
    try:
        responseDict = {}

        recipe = cursor.query(Recipe).filter_by(id=recipe_id).first()
        if not recipe:
            raise ValueError('No Such Recipe')

        responseDict["id"] = recipe.id
        responseDict["cook_time_in_min"] = recipe.cook_time_in_min
        responseDict["prep_time_in_min"] = recipe.prep_time_in_min
        responseDict["total_time_in_min"] = recipe.total_time_in_min
        responseDict["title"] = recipe.title
        responseDict["cuisine"] = recipe.cuisine
        responseDict["servings"] = recipe.servings
        responseDict["author_id"] = recipe.author_id
        responseDict["created_ts"] = recipe.created_ts
        responseDict["updated_ts"] = recipe.updated_ts

        nutritioninformation = cursor.query(NutritionInformation).filter_by(recipe_id=recipe_id).first()
        nutriDict = {}
        nutriDict["calories"] = nutritioninformation.calories
        nutriDict["cholesterol_in_mg"] = str(nutritioninformation.cholesterol_in_mg)
        nutriDict["sodium_in_mg"] = int(nutritioninformation.sodium_in_mg)
        nutriDict["carbohydrates_in_grams"] = str(nutritioninformation.carbohydrates_in_grams)
        nutriDict["protein_in_grams"] = str(nutritioninformation.protein_in_grams)

        responseDict["nutrition_information"] = nutriDict

        ingredients = cursor.query(Ingredients).filter_by(recipe_id=recipe_id).all()
        ingridList = []
        for ingrid in ingredients:
            ingridList.append(ingrid.ingredient)

        responseDict["ingredients"] = ingridList

        steps = cursor.query(Steps).filter_by(recipe_id=recipe_id).all()
        stepList= []
        for step in steps:
            stepdict = {}
            stepdict["position"]= int(step.position)
            stepdict["items"]= str(step.items)
            stepList.append(stepdict)

        responseDict["steps"] = stepList

        return responseDict
    except Exception as e:
        logger.debug("Exception in getting recipe: " + str(e))
        raise Exception(str(e))


def delete_recipy(cursor, recipe_id):
    try:
        recipe = cursor.query(Recipe).filter_by(id=recipe_id).first()
        if not recipe:
            raise ValueError('No Such Recipe')
        cursor.delete(recipe)

        nutritioninformation = cursor.query(NutritionInformation).filter_by(recipe_id=recipe_id).first()
        cursor.delete(nutritioninformation)

        ingredients = cursor.query(Ingredients).filter_by(recipe_id=recipe_id).all()
        for ingrid in ingredients:
            cursor.delete(ingrid)

        steps = cursor.query(Steps).filter_by(recipe_id=recipe_id).all()
        for step in steps:
            cursor.delete(step)
        
        cursor.commit()
        return Response(status=204, mimetype='application/json')


    except Exception as e:
        logger.debug("Exception in deleting recipe: " + str(e))
        raise Exception(str(e))
