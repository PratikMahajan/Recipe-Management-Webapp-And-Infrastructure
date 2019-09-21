.PHONY: db-shell db-setup \
	run 


DB_USER ?= recp-dev
DB_PASSWORD ?= secretpassword

db-shell:
	mysql -u $DB_USER -p $DB_PASSWORD

db-setup:
	sudo ./deploy/desetup.sh

run:
	./gunicornstart.sh