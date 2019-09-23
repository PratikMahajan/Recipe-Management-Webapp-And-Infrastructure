#!/bin/bash

echo "Changing ROOT password"
mysql -uroot -e "use mysql; SET PASSWORD FOR 'root'@'localhost' = PASSWORD('${DB_ROOT_PASSWORD}'); flush privileges;"


echo "Adding Database"
mysql -uroot --password=${DB_ROOT_PASSWORD} -e "CREATE DATABASE ${DATABASE_NAME};"


if [ $? -ne 0 ]; then
    echo "unsuccessful"
    exit 1
fi

echo "Creating User"
mysql -uroot -p${DB_ROOT_PASSWORD} -e "CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';"


if [ $? -ne 0 ]; then
    echo "unsuccessful"
    exit 1
fi

echo "Granting ALL privileges on ${DATABASE_NAME} to ${DB_USER}!"
mysql -uroot -p${DB_ROOT_PASSWORD} -e "GRANT ALL PRIVILEGES ON ${DATABASE_NAME}.* TO '${DB_USER}'@'localhost';"
mysql -uroot -p${DB_ROOT_PASSWORD} -e "FLUSH PRIVILEGES;"

if [ $? -ne 0 ]; then
    echo "unsuccessful"
    exit 1
fi

echo "Adding tables"
mysql -u ${DB_USER} --password=${DB_PASSWORD} -e "USE ${DATABASE_NAME};
        CREATE TABLE user_info (id bigint NOT NULL AUTO_INCREMENT PRIMARY KEY, first_name varchar(128) NOT NULL,
        last_name varchar(128), email varchar(128) NOT NULL, password varchar(256) NOT NULL,
        account_created DATE NOT NULL, account_updated DATE NOT NULL, token varchar(256));"
if [ $? -ne 0 ]; then
    echo "unsuccessful"
    exit 1
fi

echo "Database Initialized successfully"

