.PHONY:
dev:
	docker-compose up -d --build

.PHONY:
clean:
	docker-compose down -v

.PHONY:
logs:
	docker-compose logs web

.PHONY:
open:
	open http://localhost:8004/ping

.PHONY:
install:
	pip install -r project/requirements.txt

.PHONY:
db-init:
	docker-compose exec web alembic revision --autogenerate -m "init"

.PHONY:
add-migration:
	docker-compose exec web alembic revision --autogenerate -m "$(name)"

.PHONY:
migrate:
	docker-compose exec web alembic upgrade head

.PHONY:
test:
	pytest

.PHONY:
check:
	mypy project/app
	mypy project/tests
	flake8 project
	isort project
	black project
