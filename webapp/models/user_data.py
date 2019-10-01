from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import bcrypt
import random
import string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from config.envvar import *
import json
from config.logger import *


Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))

class User(Base):
    __tablename__ = "user_info"
    id = Column(String(128), primary_key=True)
    first_name = Column(String(32))
    last_name = Column(String(32))
    password = Column(String(128))
    email_address = Column(String(128), index=True , unique=True)
    account_created = Column(String(64))
    account_updated = Column(String(64))

    def bcrypt_salt_hash(self, password):
        salt = bcrypt.gensalt(rounds=16)
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt)

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def gen_auth_token(self, exp=600):
        s=Serializer(secret_key, expires_in=exp)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data=s.loads(token)
        except SignatureExpired:
            logger.debug("Exception in verify_auth_token: Signature Expired")
            return None
        except BadSignature:
            logger.debug("Exception in verify_auth_token: Bad Signature")
            return None
        user_id = data['id']
        return user_id


engine = create_engine('mysql+pymysql://'+db_config["DB_USER"]+':'+db_config["DB_PASSWORD"]+'@'+db_config["DB_HOST"]+'/'
                       + db_config["DB_NAME"])

Base.metadata.create_all(engine)