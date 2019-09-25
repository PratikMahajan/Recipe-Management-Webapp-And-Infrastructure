from models.user_data import Base, User
from flask import Flask,Response, jsonify, request, abort,g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import uuid
from datetime import datetime
from flask_httpauth import HTTPBasicAuth
from config.loggingfilter import *
from config.envvar import *

auth = HTTPBasicAuth()

engine = create_engine('mysql+pymysql://'+db_config["DB_USER"]+':'+db_config["DB_PASSWORD"]+'@'+db_config["DB_HOST"]+'/'
                       + db_config["DB_NAME"], echo=True)

app = Flask(__name__)


def get_db():
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


@auth.verify_password
def verify_password(username_or_token, password):
    # Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = get_db().query(User).filter_by(id=user_id).one()
    else:
        user = get_db().query(User).filter_by(email_address=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/v1/user', methods=['POST'])
def new_user():
    cursor=get_db()
    username = request.json.get('email_address')
    password = request.json.get('password')
    if username is None or password is None:
        status={'ERROR': 'Missing Arguments'}
        return Response(json.dumps(status), status=400, mimetype='application/json')
        
    if session.query(User).filter_by(email_address = username).first() is not None:
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


@app.route('/v1/user/self', methods=['GET'])
@auth.login_required
def get_user():
    return jsonify({'id': g.user.id, 'first_name': g.user.first_name, 'last_name': g.user.last_name,
                    'email_address': g.user.email_address, 'account_created': g.user.account_created,
                    'account_updated': g.user.account_updated}), 200


@app.route('/v1/user/self', methods=['PUT'])
@auth.login_required
def update_user():
    cursor=get_db()
    if ((request.json.get('id') is not  None) or (request.json.get('email_address') is not None) or
            (request.json.get('account_created') is not None) or (request.json.get('account_updated') is not None)):
        return Response(status=400, mimetype='application/json')
    else:
        if request.json.get('first_name') is not None:
            g.user.first_name=request.json.get('first_name')
        if request.json.get('last_name') is not None:
            g.user.last_name=request.json.get('last_name')
        if request.json.get('password') is not None:
            g.user.bcrypt_salt_hash(request.json.get('password'))
        g.user.account_updated = str(datetime.now())
        cursor.commit()
        return jsonify({}), 204


@app.route('/health', methods=['GET', 'POST'])
@disable_logging
def health_probe() -> Response:
    status = dict()
    status["ok"] = True
    return Response(json.dumps(status), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)