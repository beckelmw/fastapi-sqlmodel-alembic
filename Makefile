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
add-migration: ## Create migration. Usage make add-migration name=""
	@test -n "$(name)" || (echo 'A name must be defined for the migration. Ex: make add-migration name=init' && exit 1)
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
	mypy ./app ./tests
	flake8 ./app ./tests
	isort ./app ./tests
	black ./app ./tests

##@ Misc
.PHONY logs:
logs: ## Get web logs
	docker-compose logs web

.PHONY install:
install: ## Install python dependencies
	pip install -r requirements.txt

.PHONY freeze:
freeze: ## Save current dependencies to requirements.txt
	pip freeze requirements.txt

.PHONY: help
help: ## Help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)