files_to_fmt 	?= app
files_to_check 	?= app

run:
	uvicorn app:create_app --host localhost --reload --port 5000


migrate:
	poetry run python -m scripts.migrate

docker_up:
	docker-compose up --build -d

isort:
	isort ${files_to_fmt}

black:
	black ${files_to_fmt}

black_check:
	black --check ${files_to_check}