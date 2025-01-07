# Makefile

.PHONY: help build up down logs test clean db-shell db-backup db-restore

# Default target
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.?## .+$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build all containers
	docker-compose build

build-no-cache: ## Stop all containers
	docker-compose build --no-cache

up: ## Start all containers in detached mode
	docker-compose up -d

down: ## Stop all containers
	docker-compose down

logs: ## View logs
	docker-compose logs -f

remove-images-all: ## Remove all images
	docker-compose rm -f

prune: ## Remove all stopped containers, dangling images, and unused networks and volumes
	docker system prune -f

prune-volumes:
	docker volume prune -f

test: ## Run tests
	docker-compose exec backend pytest

clean: ## Remove all containers, networks, and volumes
	docker-compose down -v --remove-orphans

db-shell: ## Access PostgreSQL shell
	docker-compose exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

db-backup: ## Backup the database
	docker-compose exec db pg_dump -U $(POSTGRES_USER) $(POSTGRES_DB) > backup_$(shell date +%Y%m%d_%H%M%S).sql

db-restore: ## Restore the database from a backup file
	@echo "Usage: make db-restore FILE=backup_file.sql"
	@test $(FILE) || (echo "Please specify a backup file with FILE=backup_file.sql" && exit 1)
	docker-compose exec -T db psql -U $(POSTGRES_USER) $(POSTGRES_DB) < $(FILE)
