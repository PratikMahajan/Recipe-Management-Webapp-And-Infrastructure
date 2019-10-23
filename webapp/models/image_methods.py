import uuid
from flask import Response, jsonify
import boto3, botocore
import os
from config.s3envvar import S3_BUCKET, S3_KEY, S3_SECRET
from io import BytesIO

os.environ['AWS_PROFILE'] = "dev"
os.environ['AWS_DEFAULT_REGION'] = "us-east-1"

session = boto3.Session(profile_name='dev')

s3 = boto3.client ("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)

def upload_image(files, bucket_name):

    try:

        s3.upload_fileobj(
                BytesIO(files), 
                bucket_name,
                files.filename, 
                ExtraArgs={ 
                    "ContentType": files.content_type
                }
        )

    except Exception as e:
        raise Exception(str(e))

    return "{}{}".format(app.s3config["S3_LOCATION"], files.filename)

