DOCKER_ADDRESS  ?= localhost

.DEFAULT_GOAL   := help

##@ General

.PHONY: help
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: \033[36mmake <target>\033[0m\n\nAwailable targets:\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

.PHONY: dev-compose
dev-compose: ## Compose full environment emulation using docker-compose.
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build

.PHONY: clean
clean: ## Remove all temporary files.
	git clean -fdX \
		--exclude '!.env' \
		--exclude '!.venv' \
		--exclude '!.venv/**' \
		--exclude '!.vscode' \
		--exclude '!.vscode/**' \
		--exclude '!.python-version'

##@ Code style

.PHONY: lint
lint: ## Run the linters and reformat the code if possible.
	poetry run pre-commit run --all-files
