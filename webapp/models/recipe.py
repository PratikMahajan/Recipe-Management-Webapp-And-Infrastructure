from sqlalchemy import Column,Integer,String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config.envvar import *

Base = declarative_base()

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

engine = create_engine('mysql+pymysql://'+db_config["DB_USER"]+':'+db_config["DB_PASSWORD"]+'@'+db_config["DB_HOST"]+'/'
                       + db_config["DB_NAME"])

Base.metadata.create_all(engine)
