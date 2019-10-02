from sqlalchemy import Column,Integer,String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from config.envvar import *

Base = declarative_base()

class NutritionInformation(Base):
    __tablename__ = "nutritioninformation"
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(String(128),index=True)
    calories = Column(Integer)
    cholesterol_in_mg = Column(Float(10, 2))
    sodium_in_mg = Column(Integer)
    carbohydrates_in_grams = Column(Float(10, 2))
    protein_in_grams = Column(Float(10, 2))

engine = create_engine('mysql+pymysql://'+db_config["DB_USER"]+':'+db_config["DB_PASSWORD"]+'@'+db_config["DB_HOST"]+'/'
                       + db_config["DB_NAME"])

Base.metadata.create_all(engine)

