#!/bin/bash

echo "Changing ROOT password"
mysql -uroot -e "use mysql; SET PASSWORD FOR 'root'@'localhost' = PASSWORD('${DB_ROOT_PASSWORD}'); flush privileges;"

echo "Adding Database"
mysql -uroot --password=${DB_ROOT_PASSWORD} -e "CREATE DATABASE ${DATABASE_NAME};"

if [ $? -ne 0 ]; then
    echo "Make sure to not use '-' in database name"
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

echo "Database Initialized successfully"
