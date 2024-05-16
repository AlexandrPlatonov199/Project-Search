run:
	uvicorn app:create_app --host localhost --reload --port 5000


migrate:
	poetry run python -m scripts.migrate