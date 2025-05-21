# Project build and development workflow management
# See README.md for usage instructions

.PHONY: all clean build_lambda_requirements build_lambda_src format lint types test check docs security-check help init-pre-commit ci bandit gitleaks secrets-check dependency-check

# Configuration
DIST_DIR := dist/lambda
AWS_DIR := ./etc/infra/aws
VERSION := $(shell uvx --from=toml-cli toml get --toml-path=pyproject.toml project.version)
PROJECT_NAME := $(shell uvx --from=toml-cli toml get --toml-path=pyproject.toml project.name)
TEST_PATH ?= tests
COVERAGE_MODULE ?= src
PYTEST_ARGS ?= -vvs
RUFF_ARGS ?= --fix

# Build targets
all: clean build_lambda_requirements build_lambda_src

clean:
	rm -rf $(DIST_DIR)

build_lambda_requirements:
	@echo "Building lambda requirements layer..."
	mkdir -p $(DIST_DIR)/requirements/python
	uv export --no-dev --no-editable --no-color | sed 's/\x1b\[[0-9;]*m//g' > dist/requirements.txt
	uv pip -n install --requirements=dist/requirements.txt --target=dist/lambda/requirements/python
	cd $(DIST_DIR)/requirements && zip -9 -q -r ../$(PROJECT_NAME)-requirements-layer-$(VERSION).zip python/
	@echo "Lambda requirements layer built to $(DIST_DIR)/$(PROJECT_NAME)-requirements-layer-$(VERSION).zip"

build_lambda_src:
	@echo "Building lambda function source..."
	uv build --out-dir=$(DIST_DIR)/src
	mv $(DIST_DIR)/src/*.whl $(DIST_DIR)/$(PROJECT_NAME)-$(VERSION).zip
	@echo "Lambda function source built to $(DIST_DIR)/$(PROJECT_NAME)-$(VERSION).zip"

# Development targets
format:
	uv run ruff format src/ $(TEST_PATH)/

lint:
	uv run ruff check $(RUFF_ARGS) src/ $(TEST_PATH)/

types:
	uv run mypy src/

test:
	uv run pytest --cov=$(COVERAGE_MODULE) $(PYTEST_ARGS) $(TEST_PATH)

# Security checks
bandit:
	@echo "Running security checks with Bandit..."
	uv run bandit -r src/ -c pyproject.toml

# Comprehensive check (all verification steps)
check: format lint types test bandit
	@echo "All checks completed successfully!"

# Deployment (OpenTofu/Terraform)
init:
	cd $(AWS_DIR) && tofu init

init-reconfigure:
	cd $(AWS_DIR) && tofu init -reconfigure

plan:
	cd $(AWS_DIR) && tofu plan

apply:
	cd $(AWS_DIR) && tofu apply

destroy:
	cd $(AWS_DIR) && tofu destroy

# Help
help:
	@echo "Available targets:"
	@echo "  all                                            - Clean and build Lambda package"
	@echo "  clean                                          - Remove build artifacts"
	@echo "  build_*                                        - Build Lambda components"
	@echo "  format                                         - Format code with ruff"
	@echo "  lint                                           - Run linting with ruff"
	@echo "  types                                          - Type-check with mypy"
	@echo "  test                                           - Run tests with pytest"
	@echo "  check                                          - Run all code quality checks"
	@echo "  bandit                                         - Run Bandit security scanner"
	@echo "  init, init-reconfigure, plan, apply, destroy   - Manage infrastructure with OpenTofu"
	@echo "  help                                           - Show this help message"