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

class Recipe(Base):
    __tablename__ = "recipe"
    id = Column(String(128), primary_key=True)
    cook_time_in_min = Column(Integer)
    prep_time_in_min = Column(Integer)
    total_time_in_min = Column(Integer)
    title = Column(String(256))
    cuisine = Column(String(64))
    servings = Column(Integer)
    author_id = Column(String(128))
    created_ts = Column(String(64))
    updated_ts = Column(String(64))


class Steps(Base):
    __tablename__ = "steps"
    id = Column(INTEGER(zerofill=True),
                Sequence('article_aid_seq', start=1001, increment=1), primary_key=True)
    recipe_id = Column(String(128))
    position = Column(Integer)
    items = Column(String(256))


class NutritionInformation(Base):
    __tablename__ = "nutritioninformation"
    id = Column(INTEGER(zerofill=True),
                Sequence('article_aid_seq', start=1001, increment=1), primary_key=True)
    recipe_id = Column(String(128))
    calories = Column(Integer)
    cholesterol_in_mg = Column(Float(10, 2))
    sodium_in_mg = Column(Integer)
    carbohydrates_in_grams = Column(Float(10, 2))
    protein_in_grams = Column(Float(10, 2))



engine = create_engine('mysql+pymysql://'+db_config["DB_USER"]+':'+db_config["DB_PASSWORD"]+'@'+db_config["DB_HOST"]+'/'
                       + db_config["DB_NAME"])

Base.metadata.create_all(engine)