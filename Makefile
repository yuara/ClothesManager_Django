
ARG := "foo"

.PHONY: env run shell mk migr remg user reuserlite test up down clean log db web scrape

env:
	pipenv shell

run:
	python services/web/manage.py runserver

enshell:
	python services/web/manage.py shell

enmk:
	python services/web/manage.py makemigrations

enmg:
	python services/web/manage.py migrate

enuser:
	python services/web/manage.py createsuperuser

remg: mk migr

reuser: mk migr user

lite:
	sqlite3 services/web/db.sqlite3

up:
	docker-compose up -d --build

down:
	docker-compose down -v

start:
	docker-compose start

stop:
	docker-compose stop

clean:
	docker-compose down --rmi all --volumes

log:
	docker-compose logs -f

db:
	docker-compose exec dev-db psql --username=cmuser --dbname=cm

web:
	docker-compose exec dev-web sh

shell:
	docker-compose exec dev-web python manage.py shell

# make test ARG=accounts
test:
	docker-compose exec dev-web python manage.py test --debug-mode ${ARG}

sc:
	docker-compose exec dev-scrapyd curl http://dev-scrapyd:6800/schedule.json -d project=scraping -d spider=forecast

mk:
	docker-compose exec dev-web python manage.py makemigrations

mg:
	docker-compose exec dev-web python manage.py migrate

user:
	docker-compose exec dev-web python manage.py createsuperuser

pdup:
	docker-compose -f docker-compose.prod.yml up -d --build

pddown:
	docker-compose -f docker-compose.prod.yml down -v

pdlog:
	docker-compose -f docker-compose.prod.yml logs -f

pdmg:
	docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

pdst:
	docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

pdsc:
	docker-compose -f docker-compose.prod.yml exec scrapyd curl http://scrapyd:6800/schedule.json -d project=scraping -d spider=forecast

pdweb:
	docker-compose -f docker-compose.prod.yml exec web sh

pddb:
	docker-compose -f docker-compose.prod.yml exec db psql --username=cmuser --dbname=cm
