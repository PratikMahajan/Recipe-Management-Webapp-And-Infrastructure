from config.loggingfilter import *
from config.logger import *
from config.envvar import *
from flask import Flask,Response, jsonify, request, abort,g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import uuid
from datetime import datetime
from flask_httpauth import HTTPBasicAuth
from config.loggingfilter import *
from config.logger import *
from config.envvar import *
import json
import re
from models.recipe import *


def round_to_5(number):
    try:
        return int(math.ceil(number / 5.0)) * 5
    except:
        raise ValueError('Incorrect Time Format')


def insert_recipe(cursor, recipeJson, authorID):
    try:
        id = str(uuid.uuid4())
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

        ingredientset = set()
        ingredientset.add(recipeJson["ingredients"])
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

        return id

    except Exception as e:
        cursor.rollback()
        logger.debug("Exception in creating recipe: "+str(e))
        raise Exception(str(e))


def get_recipe(cursor, recipe_id):
    try:
        responseDict = {}

        recipe = cursor.query(Recipe).filter_by(id=recipe_id).first()
        if not recipe:
            return False

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

        nutritioninformation = cursor.query(NutritionInformation).filter_by(id=recipe_id).first()
        nutriDict = {}
        nutriDict["calories"] = nutritioninformation.calories
        nutriDict["cholesterol_in_mg"] = nutritioninformation.cholesterol_in_mg
        nutriDict["sodium_in_mg"] = nutritioninformation.sodium_in_mg
        nutriDict["carbohydrates_in_grams"] = nutritioninformation.carbohydrates_in_grams
        nutriDict["protein_in_grams"] = nutritioninformation.protein_in_grams

        responseDict["nutrition_information"] = nutriDict

        ingredients = cursor.query(Ingredients).filter_by(id=recipe_id)
        ingridList = []
        for ingrid in ingredients:
            ingridList.append(str(ingrid[2]))

        responseDict["ingredients"] = ingridList

        steps = cursor.query(Steps).filter_by(id=recipe_id)
        stepList= []
        for step in steps:
            stepdict = {}
            stepdict["position"]= int(step[2])
            stepdict["items"]= str(step[3])
            stepList.append(stepdict)

        responseDict["steps"] = stepList

        return json.dumps(responseDict)
    except Exception as e:
        logger.debug("Exception in getting recipe: " + str(e))
        raise Exception(str(e))