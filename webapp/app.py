from models import Base, User
from flask import Flask,Response, jsonify, request, abort,g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import uuid
from datetime import datetime
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from config.loggingfilter import *

engine = create_engine('mysql+pymysql://user:user@localhost/user',echo=True)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@auth.verify_password
def verify_password(username_or_token, password):
    #Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id = user_id).one()
    else:
        user = session.query(User).filter_by(email_address = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

@app.route('/v1/user', methods = ['POST'])
def new_user():
    username = request.json.get('email_address')
    password = request.json.get('password')
    if username is None or password is None:
        print("missing arguments")
        abort(400) 
        
    if session.query(User).filter_by(email_address = username).first() is not None:
        print("existing user")
        abort(400)

    user = User(id=str(uuid.uuid4()),first_name =request.json.get('first_name'),last_name=request.json.get('last_name'),email_address = username,account_created=str(datetime.now()),account_updated=str(datetime.now()))
    user.bcrypt_salt_hash(password)
    session.add(user)
    session.commit()
    return jsonify({ 'id':user.id,'first_name':user.first_name,'last_name':user.last_name,'email_address':user.email_address,'account_created': user.account_created,'account_updated':user.account_updated}), 201

@app.route('/health', methods=['GET', 'POST'])
@disable_logging
def health_probe() -> Response:
    status = dict()
    status["ok"] = True
    return Response(json.dumps(status), status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
