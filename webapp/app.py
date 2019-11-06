from models.user_data import Base, User
from models.recipe import *
from models.ingredients import *
from models.nutritioninformation import *
from models.steps import *
from models.image import *
from models.recipe_methods import *
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
import boto3, botocore
import time
from statsd import StatsClient

allowed_extentions=set(['png','jpg','jpeg'])
auth = HTTPBasicAuth()

engine = create_engine('mysql+pymysql://'+db_config["DB_USER"]+':'+db_config["DB_PASSWORD"]+'@'+db_config["DB_HOST"]+'/'
                       + db_config["DB_NAME"], pool_size=20)

s3_resource = boto3.resource("s3", aws_access_key_id=aws_config["AWS_ACCESS_KEY_ID"], aws_secret_access_key=aws_config["AWS_SECRET_ACCESS_KEY"])

statsd = StatsClient(host='localhost', port=8125, prefix='webapp2')

app = Flask(__name__)

def get_db():
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


cursor = get_db()


def check_username(email):
    if re.search("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
        return True
    return False

def allowed_file(name):
    return '.' in name and name.rsplit('.', 1)[1] in allowed_extentions

def check_password(password):
    if re.search('^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])', password):
        return True
    return False


@auth.verify_password
def verify_password(username_or_token, password):
    try:
        user_id = User.verify_auth_token(username_or_token)
        if user_id:
            user = cursor.query(User).filter_by(id=user_id).one()
        else:
            user = cursor.query(User).filter_by(email_address=username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        g.user = user
        return True
    except Exception as e:
        logger.debug("Exception in verify_password: "+str(e))
        return False


@app.route('/token')
@auth.login_required
def get_auth_token():
    try:
        token = g.user.generate_auth_token()
        status = {'token': token.decode('ascii')}
        return Response(json.dumps(status), status=200, mimetype='application/json')
    except Exception as e:
        logger.debug("Exception in get_auth_token: "+str(e))
        return Response(status=403, mimetype='application/json')


@app.route('/v1/user', methods=['POST'])
def new_user():
    try:
        statsd.incr('cntrcreateUser')
        with statsd.timer('createUser1'):
            username = request.json.get('email_address')
            password = request.json.get('password')

            if not check_username(username):
                status = {'ERROR': 'Invalid Email'}
                return Response(json.dumps(status), status=400, mimetype='application/json')

            if not check_password(password):
                status = {'ERROR': 'Insecure Password'}
                return Response(json.dumps(status), status=400, mimetype='application/json')

            if username is None or password is None:
                status={'ERROR': 'Missing Arguments'}
                return Response(json.dumps(status), status=400, mimetype='application/json')

            if cursor.query(User).filter_by(email_address=username).first() is not None:
                status = {'ERROR': 'User Error'}
                return Response(json.dumps(status), status=400, mimetype='application/json')

            user = User(id=str(uuid.uuid4()), first_name=request.json.get('first_name'), last_name=request.json.get('last_name'),
                        email_address=username, account_created=str(datetime.now()), account_updated=str(datetime.now()))
            user.bcrypt_salt_hash(password)
            cursor.add(user)
            cursor.commit()
            return jsonify({'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name,
                        'email_address': user.email_address, 'account_created': user.account_created,
                        'account_updated': user.account_updated}), 201
    except Exception as e:
        cursor.rollback()
        status = {'ERROR': str(e)}
        logger.debug("Exception in creating user /v1/user: " + str(e))
        return Response(json.dumps(status), status=400, mimetype='application/json')


@app.route('/v1/user/self', methods=['GET'])
@auth.login_required
@statsd.timer('getUser')
def get_user():
    try:
        statsd.incr('cntrgetUser')
        return jsonify({'id': g.user.id, 'first_name': g.user.first_name, 'last_name': g.user.last_name,
                        'email_address': g.user.email_address, 'account_created': g.user.account_created,
                        'account_updated': g.user.account_updated}), 200
    except Exception as e:
        logger.debug("Exception in getting user get_user() /v1/user/self/: " + str(e))
        return Response(status=400, mimetype='application/json')


@app.route('/v1/user/self', methods=['PUT'])
@auth.login_required
@statsd.timer('updateUser')
def update_user():
    try:
        statsd.incr('cntrupdateUser')
        if ((request.json.get('id') is not  None) or (request.json.get('email_address') is not None) or
                (request.json.get('account_created') is not None) or (request.json.get('account_updated') is not None)):
            return Response(status=400, mimetype='application/json')
        else:
            if request.json.get('first_name') is not None:
                g.user.first_name = request.json.get('first_name')
            if request.json.get('last_name') is not None:
                g.user.last_name = request.json.get('last_name')
            if request.json.get('password') is not None:
                if not check_password(request.json.get('password')):
                    status = {'ERROR': 'Insecure Password'}
                    return Response(json.dumps(status), status=400, mimetype='application/json')
                g.user.bcrypt_salt_hash(request.json.get('password'))
            g.user.account_updated = str(datetime.now())
            cursor.commit()
            return Response(status=204, mimetype='application/json')
    except Exception as e:
        cursor.rollback()
        logger.debug("Exception in updating user update_user() /v1/user/self/: " + str(e))
        return Response(status=400, mimetype='application/json')


@app.route('/v1/recipe/', methods=['POST'])
@auth.login_required
@statsd.timer('createRecipe')
def add_recipe():
    try:
        statsd.incr('cntrcreateRecipe')
        retJson = insert_recipe(cursor,request.json,g.user.id)
        cursor.commit()
        return Response(json.dumps(retJson), status=201, mimetype='application/json')

    except Exception as e:
        logger.debug("Exception while adding recipe /v1/recipe/: " + str(e))
        return Response(status=400, mimetype='application/json')


@app.route('/v1/recipe/<id>', methods=['GET'])
@statsd.timer('getRecipe')
def get_recipe(id):
    try:
        statsd.incr('cntrgetRecipe')
        resp,status=get_recipy(cursor,id)
        return jsonify(resp),status
    except Exception as e:
        status = {'ERROR': str(e)}
        logger.debug("Exception while getting recipe /v1/recipe/<id>: " + str(e))
        return Response(json.dumps(status), status=404, mimetype='application/json')


@app.route('/v1/recipe/<id>', methods=['DELETE'])
@auth.login_required
@statsd.timer('deleteRecipe')
def delete_recipe(id):
    try:
        statsd.incr('cntrdeleteRecipe')
        resp,status=delete_recipy(cursor, id,g.user.id)
        return jsonify(resp),status

    except Exception as e:
        status = {'ERROR': str(e)}
        logger.debug("Exception while deleting recipe /v1/recipe/{id}: " + str(e))
        return Response(json.dumps(status), status=400, mimetype='application/json')


@app.route('/v1/recipe/<id>', methods=['PUT'])
@auth.login_required
@statsd.timer('updateRecipe')
def update_recipe(id):
    try:
        statsd.incr('cntrupdateRecipe')
        recJson,status = get_recipy(cursor, id)
        if status != 200:
            return jsonify(recJson),status
        recpID = recJson["id"]
        createdTime = recJson["created_ts"]

        resp,stat =  delete_recipy(cursor, id,g.user.id)
        if stat==204:
            retJson = insert_recipe(cursor,request.json,g.user.id, recpID, createdTime)
            cursor.commit()
            return Response(json.dumps(retJson), status=204, mimetype='application/json')
        else:
            return jsonify(resp),stat

    except Exception as e:
        cursor.rollback()
        status = {'ERROR': str(e)}
        logger.debug("Exception while updating recipe /v1/recipe/{id}: " + str(e))
        return Response(json.dumps(status), status=400, mimetype='application/json')


@app.route('/v1/recipe/<id>/image', methods=['POST'])
@auth.login_required
@statsd.timer('addImage')
def add_image(id):
    try:
        statsd.incr('cntraddImage')
        if 'file' not in request.files:
            status={'ERROR':'No File part'}
            return jsonify(status), 400
        filee=request.files['file']
        if filee.filename=='':
            status={'ERROR':'No File selected'}
            return jasonify(status),400
        if filee and allowed_file(filee.filename):
            recJson,status = get_recipy(cursor, id)
            if status != 200:
                return jsonify(recJson),status
            if recJson["author_id"]!=g.user.id:
               status = {'ERROR':'UnAuthorized'}
               return jsonify(status), 401
            imgIds=delete_img_recipe(cursor,id)
            for imgId in imgIds:
                s3_resource.Bucket(aws_config["RECIPE_S3"]).delete_objects(Delete={'Objects':[{'Key':imgId}]})
            imgId=str(uuid.uuid4())
            #s3_resource = boto3.resource('s3')
            s3_resource.Bucket(aws_config["RECIPE_S3"]).put_object(Key=imgId,Body=filee)
            s3Obj=boto3.client('s3').head_object(Bucket=aws_config["RECIPE_S3"],Key=imgId)
            img_url="https://s3.amazonaws.com/"+aws_config["RECIPE_S3"]+"/"+imgId
            img=Image(id=imgId,recipe_id=id,url=img_url,img_metadata=str(s3Obj))
            cursor.add(img)
            cursor.commit()
            return jsonify({'id':img.id,'url':img.url}), 201
        else:
            status={'ERROR':'only .png,.jpg,jpeg files are supported'}
            return jsonify(status), 400
    except Exception as e:
        cursor.rollback()
        status = {'ERROR': str(e)}
        logger.debug("Exception while adding image /v1/recipe/<id>/image: " + str(e))
        return Response(json.dumps(status), status=400, mimetype='application/json')

@app.route('/v1/recipe/<recipeId>/image/<imageId>', methods=['DELETE'])
@auth.login_required
@statsd.timer('deleteImage')
def delete_image(recipeId,imageId):
    try:
        statsd.incr('cntrdeleteImage')
        recJson,status = get_recipy(cursor, recipeId)
        if status != 200:
            return jsonify(recJson),status
        if recJson["author_id"]!=g.user.id:
           status = {'ERROR':'UnAuthorized'}
           return jsonify(status), 401
        resp, status = delete_img(cursor,imageId,recipeId)
        if status != 204:
            return jsonify(resp),status
        s3_resource.Bucket(aws_config["RECIPE_S3"]).delete_objects(Delete={'Objects':[{'Key':imageId}]})
        return jsonify(resp),status

    except Exception as e:
        status = {'ERROR': str(e)}
        logger.debug("Exception while deleting recipe image /v1/recipe/<recipeId>/image/<imageId>: " + str(e))
        return Response(json.dumps(status), status=400, mimetype='application/json')

        
@app.route('/v1/recipe/<recipeId>/image/<imageId>', methods=['GET'])
@statsd.timer('getImage')
def get_image(recipeId,imageId):
    try:
        statsd.incr('cntrgetImage')
        resp,status=get_img(cursor,imageId,recipeId)
        return jsonify(resp),status
    except Exception as e:
        status = {'ERROR': str(e)}
        logger.debug("Exception while getting recipe /v1/recipe/<recipeId>/image/<imageId>: " + str(e))
        return Response(json.dumps(status), status=404, mimetype='application/json')
        
@app.route('/health', methods=['GET', 'POST'])
@disable_logging
def health_probe() -> Response:
    status = dict()
    status["ok"] = True
    return Response(json.dumps(status), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
