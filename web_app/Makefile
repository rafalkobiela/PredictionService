.PHONY: build run clean alembic-migrate alembic-revision test lint lint-flake8 lint-bandit requirements

build:
	docker-compose build

run:
	docker-compose up web_app

clean:
	docker-compose down --rmi all

alembic-migrate:
	docker-compose run --rm web_app_tests sh -c '/usr/local/bin/wait && alembic upgrade head'

alembic-revision: alembic-migrate
	docker-compose run --rm web_app_tests sh -c '/usr/local/bin/wait && alembic revision --autogenerate'
	sudo chown -R $(USER):$(USER) alembic

requirements:
	docker-compose run --rm --no-deps web_app_tests pip-compile
	sudo chown $(USER):$(USER) requirements.txt

test:
	docker-compose run --rm web_app_tests

lint: lint-flake8 lint-bandit

lint-flake8:
	docker-compose run --rm --no-deps web_app_tests flake8 src
	docker-compose run --rm --no-deps web_app_tests flake8 --ignore E501 tests

lint-bandit:
	docker-compose run --rm --no-deps web_app_tests bandit -r ./src
