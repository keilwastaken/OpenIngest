# Simple OpenIngest Makefile

.PHONY: help install test run build clean

help: ## Show help
	@echo "OpenIngest - Simple commands:"
	@echo ""
	@echo "  install     Install with uv"
	@echo "  test        Run tests"  
	@echo "  run         Process documents/"
	@echo "  build       Build Docker image"
	@echo "  clean       Clean up"

install: ## Install with uv
	uv sync

test: ## Run tests
	uv run pytest

run: ## Process documents with CLI
	mkdir -p documents processed
	uv run openingest documents/ -o processed/ --verbose

build: ## Build Docker image  
	docker build -t openingest .

clean: ## Clean up
	rm -rf processed/ .pytest_cache/ dist/ *.egg-info/
	docker system prune -f