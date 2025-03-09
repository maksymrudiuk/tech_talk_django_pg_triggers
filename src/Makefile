#!/usr/bin/make -f

.PHONY: format
format:
	ruff check . --fix

.PHONY: runserver
runserver:
	@python3 manage.py runserver 0.0.0.0:8000 --configuration=Local

.PHONY: migrate
migrate:
	@python3 manage.py migrate --configuration=Local

.PHONY: migrations
migrations:
	@python3 manage.py makemigrations --configuration=Local

.PHONY: shell
shell:
	@python3 manage.py shell --configuration=Local

.PHONY: collectstatic
collectstatic:
	@python3 manage.py collectstatic --noinput --configuration=Local

.PHONY: install
install:
	cd ../ && uv sync --no-install-project && cd src/


.PHONY: setup
setup:
	make install
	make migrate
	make collectstatic
	@python3 manage.py createsuperuser --noinput --configuration=Local