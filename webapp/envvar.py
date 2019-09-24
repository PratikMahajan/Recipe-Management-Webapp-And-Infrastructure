import os

db_config() = dict()
db_config["DB_USER"] = os_environ['DB_USER']
db_config["DB_PASSWORD"] = os_environ['DB_ROOT_PASSWORD']
db_config["DB_NAME"] = os_environ['DATABASE_NAME']

