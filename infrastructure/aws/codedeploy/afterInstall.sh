#!/bin/bash


sudo chown -R centos:centos /home/centos/webapp/
pip3 install -r /home/centos/webapp/scripts/requirements.txt --user


cd /home/centos/webapp
./gunicornstart.sh
./gunicornstart.sh

#read -d '' data <<EOF
#DB_USER=$DB_USER
#DB_PASSWORD=$DB_PASSWORD
#DATABASE_NAME=$DATABASE_NAME
#DB_HOST=$DB_HOST
#EOF
#
#sudo echo "$data" >> /etc/environment
#
#source /etc/environment