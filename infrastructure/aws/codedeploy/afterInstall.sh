#!/bin/bash


sudo chown -R centos:centos /home/centos/webapp/
pip3 install -r /home/centos/webapp/scripts/requirements.txt --user

sudo mkdir /home/centos/logs
sudo touch /home/centos/logs/gunicorn.log
sudo tail -n 0 -f /home/centos/logs/gunicorn*.log &
sudo chown -R centos:centos /home/centos/logs/

sudo mv /home/centos/webapp/gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl status gunicorn




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