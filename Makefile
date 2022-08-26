.DEFAULT_GOAL := help

##@ Dev
.PHONY dev:
dev: ## Build docker containers
	docker-compose up -d --build

.PHONY clean:
clean: ## Remove docker containers
	docker-compose down -v

.PHONY docs:
docs: ## Open swagger docs
	open http://localhost:8004/docs


##@ DB
.PHONY add-migration:
add-migration: ## Create alembic migration. `make add-migration name=init`
	docker-compose exec web alembic revision --autogenerate -m "$(name)"

.PHONY migrate:
migrate: ## Apply alembic migrations
	docker-compose exec web alembic upgrade head

##@ Test
.PHONY test:
test: ## Run tests
	pytest

##@ Lint
.PHONY check:
check: ## mypy, flake8m, isort and black checks
	mypy project/app
	mypy project/tests
	flake8 project
	isort project
	black project

##@ Misc
.PHONY logs:
logs: ## Get web logs
	docker-compose logs web

.PHONY install:
install: ## Install python dependencies
	pip install -r project/requirements.txt

.PHONY freeze:
freeze: ## Save current dependencies to requirements.txt
	pip freeze project/requirements.txt

.PHONY: help
help: ## Help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)