.PHONY: db-shell db-setup \
	run git


DB_USER ?= recp-dev
DB_PASSWORD ?= secretpassword

db-shell:
	mysql -u $DB_USER -p $DB_PASSWORD

db-setup:
	sudo ./deploy/desetup.sh

run:
	./gunicornstart.sh

git: check-message git-push

check-message:
	@if [ -z "${m}" ]; then echo "Message must be set, use 'make git m=your_message'"; exit 1; fi

git-push:
	git add . 
	git commit -m "$m"
	git push 
