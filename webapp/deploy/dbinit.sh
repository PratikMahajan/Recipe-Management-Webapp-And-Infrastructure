#!/bin/bash

echo "Changing ROOT password"
mysql -h 127.0.0.1  -uroot -e "use mysql -h 127.0.0.1 ; SET PASSWORD FOR 'root'@'localhost' = PASSWORD('${DB_ROOT_PASSWORD}'); flush privileges;"

echo "Adding Database"
mysql -h 127.0.0.1  -uroot --password=${DB_ROOT_PASSWORD} -e "CREATE DATABASE ${DATABASE_NAME};"

if [ $? -ne 0 ]; then
    echo "Make sure to not use '-' in database name"
    exit 1
fi

echo "Creating User"
mysql -h 127.0.0.1  -uroot -p${DB_ROOT_PASSWORD} -e "CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';"

if [ $? -ne 0 ]; then
    echo "unsuccessful"
    exit 1
fi

echo "Granting ALL privileges on ${DATABASE_NAME} to ${DB_USER}!"
mysql -h 127.0.0.1  -uroot -p${DB_ROOT_PASSWORD} -e "GRANT ALL PRIVILEGES ON ${DATABASE_NAME}.* TO '${DB_USER}'@'localhost';"
mysql -h 127.0.0.1  -uroot -p${DB_ROOT_PASSWORD} -e "FLUSH PRIVILEGES;"

if [ $? -ne 0 ]; then
    echo "unsuccessful"
    exit 1
fi

#UNCOMMENT BELOW AFTER OPTIMIZING SQLALCHEMY
#echo "Adding tables"
#mysql -h 127.0.0.1  -u ${DB_USER} --password=${DB_PASSWORD} -e "USE ${DATABASE_NAME};
#        CREATE TABLE user_info (id varchar(256) NOT NULL PRIMARY KEY, first_name varchar(128) NOT NULL,
#        last_name varchar(128), email_address varchar(128) NOT NULL, password varchar(256) NOT NULL,
#        account_created DATETIME NOT NULL, account_updated DATETIME NOT NULL);"
#if [ $? -ne 0 ]; then
#    echo "unsuccessful"
#    exit 1
#fi

echo "Database Initialized successfully"
