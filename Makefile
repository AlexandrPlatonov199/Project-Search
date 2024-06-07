files_to_fmt 	?= app
files_to_check 	?= app

run:
	uvicorn app:create_app --host localhost --reload --port 5000

## Migrate database
migrate:
	poetry run python -m scripts.migrate

docker_up:
	docker-compose up --build -d

## Sort imports
isort:
	isort ${files_to_fmt}

## Format code
black:
	black ${files_to_fmt}

## Check google spec.
pylint:
	pylint ${files_to_check}

## Check code formatting
black_check:
	black --check ${files_to_check}

## Check pep8
flake8:
	flake8 ${files_to_check}


## Check pep8
ruff:
	ruff ${files_to_check}


## Check code quality
chk: check
lint: check
check: flake8 pylint ruff black_check