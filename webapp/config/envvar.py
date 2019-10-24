import os

db_config = dict()
db_config["DB_USER"] = os.environ['DB_USER']
db_config["DB_PASSWORD"] = os.environ['DB_PASSWORD']
db_config["DB_NAME"] = os.environ['DATABASE_NAME']
db_config["DB_HOST"] = os.environ["DB_HOST"]

aws_config = dict()
aws_config["AWS_ACCESS_KEY_ID"] = os.environ['AWS_ACCESS_KEY_ID']
aws_config["AWS_SECRET_ACCESS_KEY"] = os.environ['AWS_SECRET_ACCESS_KEY']
aws_config["AWS_REGION"] = os.environ["AWS_REGION"]
aws_config["RECIPE_S3"] = os.environ["RECIPE_S3"]
