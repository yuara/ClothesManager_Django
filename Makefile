
ARG = foo

.PHONY: env run shell mk migr remg user reuserlite test up down clean log sql exec

env:
	pipenv shell

run:
	python services/manage.py runserver

shell:
	python services/manage.py shell

mk:
	python services/manage.py makemigrations

migr:
	python services/manage.py migrate

user:
	python services/manage.py createsuperuser

remg: mk migr

reuser: mk migr user

lite:
	sqlite3 services/db.sqlite3

test:
	python services/manage.py test ARG

up:
	docker-compose up -d --build

down:
	docker-compose down

clean:
	docker-compose down --rmi all --volumes

log:
	docker-compose logs -f

sql:
	docker-compose exec db mysql -u ClothesManager -p

exec:
	docker-compose exec web bash
