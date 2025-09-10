.PHONY: help install migrate test run docker-build docker-up clean

help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  migrate     - Run database migrations"
	@echo "  test        - Run tests"
	@echo "  run         - Run development server"
	@echo "  docker-build - Build Docker images"
	@echo "  docker-up   - Start Docker containers"
	@echo "  clean       - Clean up temporary files"

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

test:
	pytest --cov=nal_backend

run:
	python manage.py runserver

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/

format:
	black nal_backend/
	flake8 nal_backend/

collectstatic:
	python manage.py collectstatic --noinput

createsuperuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

celery-worker:
	celery -A nal_backend worker -l info

celery-beat:
	celery -A nal_backend beat -l info