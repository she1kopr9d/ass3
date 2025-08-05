up:
	docker-compose up -d --build

down:
	docker-compose down

migrations:
	docker-compose run fastapi-service alembic revision --autogenerate

migrate:
	docker-compose run fastapi-service alembic upgrade head
	