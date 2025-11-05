.PHONY: help install migrate test lint format clean run-dev run-celery run-beat docker-up docker-down

help:
	@echo "Spontime Development Commands"
	@echo "=============================="
	@echo "install       - Install Python dependencies"
	@echo "migrate       - Run database migrations"
	@echo "test          - Run all tests (pytest + behave)"
	@echo "test-unit     - Run unit tests only"
	@echo "test-bdd      - Run BDD tests only"
	@echo "lint          - Run code linters"
	@echo "format        - Format code with black and isort"
	@echo "clean         - Remove Python cache files"
	@echo "run-dev       - Run Django development server"
	@echo "run-celery    - Run Celery worker"
	@echo "run-beat      - Run Celery beat scheduler"
	@echo "docker-up     - Start all services with Docker Compose"
	@echo "docker-down   - Stop all services"
	@echo "docker-build  - Build Docker images"
	@echo "docker-logs   - Show Docker logs"

install:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

test: test-unit test-bdd

test-unit:
	pytest

test-bdd:
	behave

lint:
	flake8 core/ spontime/
	black --check core/ spontime/
	isort --check-only core/ spontime/

format:
	black core/ spontime/
	isort core/ spontime/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage

run-dev:
	python manage.py runserver

run-celery:
	celery -A spontime worker -l info

run-beat:
	celery -A spontime beat -l info

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-build:
	docker-compose build

docker-logs:
	docker-compose logs -f

docker-migrate:
	docker-compose exec web python manage.py migrate

docker-createsuperuser:
	docker-compose exec web python manage.py createsuperuser

docker-test:
	docker-compose exec web pytest
	docker-compose exec web behave
