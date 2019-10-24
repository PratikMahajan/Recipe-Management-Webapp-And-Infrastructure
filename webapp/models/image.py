from sqlalchemy import Column,Integer,String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config.envvar import *

Base = declarative_base()

class Image(Base):
    __tablename__ = "image"
    id = Column(String(128), primary_key=True)
    recipe_id = Column(String(128),index=True)
    url = Column(String(256))
    created_date = Column(String(64))
    size = Column(String(64))
    md5  = Column(String(128))

engine = create_engine('mysql+pymysql://'+db_config["DB_USER"]+':'+db_config["DB_PASSWORD"]+'@'+db_config["DB_HOST"]+'/'
                       + db_config["DB_NAME"])

Base.metadata.create_all(engine)
