import os

db_config = dict()
db_config["DB_USER"] = os.environ['DB_USER']
db_config["DB_PASSWORD"] = os.environ['DB_ROOT_PASSWORD']
db_config["DB_NAME"] = os.environ['DATABASE_NAME']

