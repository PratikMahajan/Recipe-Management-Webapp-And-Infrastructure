#!/bin/bash

pip install -r requirements.txt --user

{
  export DB_USER=$DB_USER
  export DB_PASSWORD=$DB_PASSWORD
  export DATABASE_NAME=$DATABASE_NAME
  export DB_HOST=$DB_HOST
} >> /etc/environment

make run



