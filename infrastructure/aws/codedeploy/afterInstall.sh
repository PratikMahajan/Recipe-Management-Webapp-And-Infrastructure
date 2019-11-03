#!/bin/bash


sudo chown -R centos:centos /home/centos/webapp/
pip3 install -r /home/centos/webapp/scripts/requirements.txt --user 2>&1

dir_name=/home/centos/logs
if [ -d "$dir_name" ]; then
    echo "Removing $dir_name"
    rm -rf "$dir_name"
fi
sudo mkdir -p /home/centos/logs
sudo touch /home/centos/logs/gunicorn.log
sudo chown -R centos:centos /home/centos/logs/

sudo mv /home/centos/webapp/gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload >/dev/null 2>&1
sudo systemctl start gunicorn >/dev/null 2>&1
#sudo systemctl status gunicorn

sudo cp /home/centos/webapp/Caddyfile /etc/caddy/
sudo mv /home/centos/webapp/caddy.service /etc/systemd/system/
sudo systemctl daemon-reload >/dev/null 2>&1
sudo systemctl start caddy >/dev/null 2>&1
#sudo systemctl status caddy

echo "Perform Unit Tests"
pip3 install -r /home/centos/webapp/scripts/requirements.txt
sudo chown -R centos:centos /home/centos/webapp/test/

echo "fetching cloudwatch schema"
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/home/centos/webapp/scripts/amazon-cloudwatch-agent-schema.json -s

echo "---------After Install Script Execution Completed------------"
exit 0

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
