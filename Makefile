install:
	uv sync

build:
	uv build

package-install:
	uv tool install dist/*.whl

lint:
	uv run ruff check

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=gendiff --cov-report=xml:coverage.xml

check: 
	test lint

dev:
	uv run flask --debug --app page_analyzer:app run

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app