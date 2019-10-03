from sqlalchemy import Column,Integer,String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config.envvar import *

Base = declarative_base()

class Steps(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(String(128),index=True)
    position = Column(Integer)
    items = Column(String(256))

engine = create_engine('mysql+pymysql://'+db_config["DB_USER"]+':'+db_config["DB_PASSWORD"]+'@'+db_config["DB_HOST"]+'/'
                       + db_config["DB_NAME"])

Base.metadata.create_all(engine)

