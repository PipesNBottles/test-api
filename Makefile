POETRY=$(shell which poetry)

all: clean install lint test

clean:
	- rm -rf *.egg-info dist
	- rm local.db

install: clean
	- $(POETRY) install

lint:
	- $(POETRY) run black .
	- $(POETRY) run flake8 .
	- $(POETRY) run mypy --ignore-missing-imports --install-types .

test: clean install
	- $(POETRY) run pytest
	- rm local.db