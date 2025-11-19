# ============================================================================
# Makefile for LangFlow + watsonx.ai Demo (using uv + Python 3.11)
# ============================================================================
#
# This Makefile supports both uv (fast, modern) and pip (traditional) workflows.
# UV is recommended for faster dependency resolution and installation.
#
# Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh
#
# Usage:
#   make install       - Install with uv (or pip if uv not available)
#   make dev           - Install with dev dependencies
#   make demo          - Run interactive demo
#   make ui            - Start LangFlow UI
#   make help          - Show all commands
#
# ============================================================================

SHELL := /usr/bin/env bash

# ------- Configuration -------
PYTHON_VERSION ?= 3.11
VENV_DIR ?= venv
PROJECT_NAME := agent_langflow
PYTHON := python3.11
UV_AVAILABLE := $(shell command -v uv 2>/dev/null)

# Default goal
.DEFAULT_GOAL := help

# Platform detection
ifeq ($(OS),Windows_NT)
	VENV_BIN := $(VENV_DIR)/Scripts
	VENV_PYTHON := $(VENV_BIN)/python.exe
	VENV_ACTIVATE := $(VENV_BIN)/activate.bat
	RM := del /Q /F
	RMDIR := rmdir /S /Q
else
	VENV_BIN := $(VENV_DIR)/bin
	VENV_PYTHON := $(VENV_BIN)/python
	VENV_ACTIVATE := $(VENV_BIN)/activate
	RM := rm -f
	RMDIR := rm -rf
endif

# Colors (Unix-like systems)
ifndef OS
	GREEN := \033[0;32m
	YELLOW := \033[1;33m
	BLUE := \033[0;34m
	RED := \033[0;31m
	NC := \033[0m
endif

# ============================================================================
# Meta Targets
# ============================================================================

.PHONY: help
help: ## Show this help message
	@echo "============================================================================"
	@echo "  LangFlow + watsonx.ai Demo - Makefile Commands (UV + Python 3.11)"
	@echo "============================================================================"
	@echo ""
	@echo "Quick Start:"
	@echo "  make install          # Install with uv (or pip fallback)"
	@echo "  make setup            # Setup credentials"
	@echo "  make demo             # Run interactive demo"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "Environment Info:"
	@echo "  Python Version: $(PYTHON_VERSION)"
	@echo "  Virtual Env: $(VENV_DIR)"
ifdef UV_AVAILABLE
	@echo "  Package Manager: uv (fast mode)"
else
	@echo "  Package Manager: pip (fallback mode)"
	@echo "  💡 Install uv for faster installs: curl -LsSf https://astral.sh/uv/install.sh | sh"
endif
	@echo ""
	@echo "============================================================================"

# ============================================================================
# Environment Setup (UV + PIP)
# ============================================================================

.PHONY: check-uv
check-uv: ## Check if uv is installed
	@if command -v uv >/dev/null 2>&1; then \
		echo "$(GREEN)✓ uv is installed: $$(uv --version)$(NC)"; \
	else \
		echo "$(YELLOW)⚠ uv not found. Will use pip (slower).$(NC)"; \
		echo "$(YELLOW)💡 Install uv for faster performance:$(NC)"; \
		echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"; \
	fi

.PHONY: check-python
check-python: ## Check if Python 3.11+ is available
	@echo "Checking Python version..."
	@if command -v python3.11 >/dev/null 2>&1; then \
		echo "$(GREEN)✓ Python 3.11 found: $$(python3.11 --version)$(NC)"; \
	elif command -v python3 >/dev/null 2>&1 && python3 -c "import sys; exit(0 if sys.version_info >= (3,11) else 1)" 2>/dev/null; then \
		echo "$(GREEN)✓ Python 3.11+ found: $$(python3 --version)$(NC)"; \
	elif command -v python >/dev/null 2>&1 && python -c "import sys; exit(0 if sys.version_info >= (3,11) else 1)" 2>/dev/null; then \
		echo "$(GREEN)✓ Python 3.11+ found: $$(python --version)$(NC)"; \
	else \
		echo "$(RED)❌ Python 3.11+ not found!$(NC)"; \
		echo "Install Python 3.11 from: https://www.python.org/downloads/"; \
		exit 1; \
	fi

$(VENV_DIR): check-python
	@echo "Creating virtual environment with Python $(PYTHON_VERSION)..."
ifdef UV_AVAILABLE
	@uv venv --python $(PYTHON_VERSION) $(VENV_DIR)
	@echo "$(GREEN)✓ Virtual environment created with uv$(NC)"
else
	@$(PYTHON) -m venv $(VENV_DIR) || python3 -m venv $(VENV_DIR) || python -m venv $(VENV_DIR)
	@echo "$(GREEN)✓ Virtual environment created with venv$(NC)"
endif

.PHONY: install
install: $(VENV_DIR) ## Install project dependencies (uv or pip)
	@echo "Installing project dependencies..."
ifdef UV_AVAILABLE
	@uv pip install -e . --python $(VENV_PYTHON)
	@echo ""
	@echo "$(GREEN)✅ Installation complete with uv! (fast mode)$(NC)"
else
	@$(VENV_PYTHON) -m pip install --upgrade pip setuptools wheel
	@$(VENV_PYTHON) -m pip install -r requirements.txt
	@echo ""
	@echo "$(GREEN)✅ Installation complete with pip!$(NC)"
	@echo "$(YELLOW)💡 Install uv for 10-100x faster installs$(NC)"
endif
	@echo ""
	@echo "To activate the environment:"
	@echo "  source $(VENV_ACTIVATE)"
	@echo ""
	@echo "Next steps:"
	@echo "  make setup     # Configure credentials"
	@echo "  make demo      # Run demo"

.PHONY: dev
dev: $(VENV_DIR) ## Install with development dependencies
	@echo "Installing project with dev dependencies..."
ifdef UV_AVAILABLE
	@uv pip install -e ".[dev]" --python $(VENV_PYTHON)
	@echo "$(GREEN)✓ Dev dependencies installed with uv$(NC)"
else
	@$(VENV_PYTHON) -m pip install --upgrade pip setuptools wheel
	@$(VENV_PYTHON) -m pip install -e ".[dev]"
	@echo "$(GREEN)✓ Dev dependencies installed with pip$(NC)"
endif

.PHONY: jupyter
jupyter: $(VENV_DIR) ## Install with Jupyter dependencies
	@echo "Installing Jupyter dependencies..."
ifdef UV_AVAILABLE
	@uv pip install -e ".[jupyter]" --python $(VENV_PYTHON)
else
	@$(VENV_PYTHON) -m pip install -e ".[jupyter]"
endif
	@echo "$(GREEN)✓ Jupyter dependencies installed$(NC)"

.PHONY: all
all: $(VENV_DIR) ## Install all dependencies (project + dev + jupyter)
	@echo "Installing all dependencies..."
ifdef UV_AVAILABLE
	@uv pip install -e ".[dev,jupyter]" --python $(VENV_PYTHON)
	@echo "$(GREEN)✓ All dependencies installed with uv$(NC)"
else
	@$(VENV_PYTHON) -m pip install --upgrade pip setuptools wheel
	@$(VENV_PYTHON) -m pip install -e ".[dev,jupyter]"
	@echo "$(GREEN)✓ All dependencies installed with pip$(NC)"
endif

.PHONY: sync
sync: check-uv ## Sync dependencies from pyproject.toml (uv only)
ifdef UV_AVAILABLE
	@echo "Syncing dependencies with uv..."
	@uv pip sync --python $(VENV_PYTHON)
	@echo "$(GREEN)✓ Dependencies synced$(NC)"
else
	@echo "$(RED)❌ 'uv sync' requires uv to be installed$(NC)"
	@echo "Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
	@echo "Or use: make install"
	@exit 1
endif

.PHONY: lock
lock: check-uv ## Generate lock file (uv only)
ifdef UV_AVAILABLE
	@echo "Generating lock file..."
	@uv pip compile pyproject.toml -o requirements.lock
	@echo "$(GREEN)✓ Lock file generated: requirements.lock$(NC)"
else
	@echo "$(YELLOW)⚠ uv not available. Using pip freeze instead...$(NC)"
	@$(VENV_PYTHON) -m pip freeze > requirements.lock
	@echo "$(GREEN)✓ Requirements frozen to: requirements.lock$(NC)"
endif

# ============================================================================
# Environment Configuration
# ============================================================================

.PHONY: setup
setup: ## Setup credentials and environment
	@echo "============================================================================"
	@echo "  Environment Setup"
	@echo "============================================================================"
	@if [ ! -f .env ]; then \
		if [ -f run.sh ]; then \
			bash run.sh setup; \
		else \
			cp .env.example .env; \
			echo "$(YELLOW)⚠ .env file created from template$(NC)"; \
			echo "Please edit .env with your watsonx.ai credentials"; \
		fi \
	else \
		echo "$(YELLOW)⚠ .env file already exists.$(NC)"; \
		read -p "Do you want to recreate it? (y/N): " confirm; \
		if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
			bash run.sh setup 2>/dev/null || (cp .env.example .env && echo "Please edit .env"); \
		else \
			echo "Keeping existing .env file."; \
		fi \
	fi

# ============================================================================
# Running Applications
# ============================================================================

.PHONY: demo
demo: ## Run interactive demo
	@echo "Starting interactive demo..."
	@if [ ! -f .env ]; then \
		echo "$(RED)❌ Error: .env file not found!$(NC)"; \
		echo "Run: make setup"; \
		exit 1; \
	fi
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) python agent_langflow.py
else
	@$(VENV_PYTHON) agent_langflow.py
endif

.PHONY: simple
simple: ## Run simple demo
	@echo "Running simple demo..."
	@if [ ! -f .env ]; then \
		echo "$(RED)❌ Error: .env file not found!$(NC)"; \
		echo "Run: make setup"; \
		exit 1; \
	fi
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) python agent_langflow.py --simple
else
	@$(VENV_PYTHON) agent_langflow.py --simple
endif

.PHONY: ui
ui: ## Start LangFlow UI
	@echo "Starting LangFlow UI..."
	@echo "UI will be available at: http://localhost:7860"
	@echo "Press Ctrl+C to stop"
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) langflow run
else
	@$(VENV_BIN)/langflow run
endif

.PHONY: ui-port
ui-port: ## Start LangFlow UI on custom port (usage: make ui-port PORT=8080)
	@echo "Starting LangFlow UI on port $(PORT)..."
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) langflow run --port $(PORT)
else
	@$(VENV_BIN)/langflow run --port $(PORT)
endif

# ============================================================================
# Testing and Validation
# ============================================================================

.PHONY: test
test: ## Run tests with pytest
	@echo "Running tests..."
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) pytest tests/ -v --cov=$(PROJECT_NAME)
else
	@$(VENV_PYTHON) -m pytest tests/ -v --cov=$(PROJECT_NAME)
endif
	@echo "$(GREEN)✓ Tests complete$(NC)"

.PHONY: test-quick
test-quick: ## Run quick tests only
	@echo "Running quick tests..."
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) pytest tests/ -v -m "not slow"
else
	@$(VENV_PYTHON) -m pytest tests/ -v -m "not slow"
endif

.PHONY: test-connection
test-connection: ## Test watsonx.ai connection
	@echo "Testing watsonx.ai connection..."
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) python agent_langflow.py --simple
else
	@$(VENV_PYTHON) agent_langflow.py --simple
endif

# ============================================================================
# Code Quality
# ============================================================================

.PHONY: lint
lint: ## Run linting with ruff
	@echo "Running ruff linter..."
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) ruff check .
else
	@$(VENV_PYTHON) -m ruff check . 2>/dev/null || $(VENV_PYTHON) -m flake8 . --max-line-length=100
endif
	@echo "$(GREEN)✓ Linting complete$(NC)"

.PHONY: format
format: ## Format code with black
	@echo "Formatting code with black..."
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) black . --line-length=100
else
	@$(VENV_PYTHON) -m black . --line-length=100
endif
	@echo "$(GREEN)✓ Formatting complete$(NC)"

.PHONY: format-check
format-check: ## Check code formatting without modifying
	@echo "Checking code formatting..."
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) black . --check --line-length=100
else
	@$(VENV_PYTHON) -m black . --check --line-length=100
endif

.PHONY: type-check
type-check: ## Run type checking with mypy
	@echo "Running mypy type checker..."
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) mypy agent_langflow.py
else
	@$(VENV_PYTHON) -m mypy agent_langflow.py
endif
	@echo "$(GREEN)✓ Type checking complete$(NC)"

.PHONY: check
check: lint format-check type-check ## Run all code quality checks
	@echo "$(GREEN)✅ All checks passed!$(NC)"

.PHONY: fix
fix: format lint ## Auto-fix code issues (format + lint)
	@echo "$(GREEN)✓ Code fixed$(NC)"

# ============================================================================
# Maintenance and Cleanup
# ============================================================================

.PHONY: clean
clean: ## Remove Python cache files and build artifacts
	@echo "Cleaning Python artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.py[co]" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@$(RM) -rf htmlcov .coverage 2>/dev/null || true
	@$(RM) -rf build dist 2>/dev/null || true
	@echo "$(GREEN)✓ Cleaned$(NC)"

.PHONY: clean-venv
clean-venv: ## Remove virtual environment
	@echo "Removing virtual environment..."
	@$(RMDIR) $(VENV_DIR) 2>/dev/null || true
	@echo "$(GREEN)✓ Virtual environment removed$(NC)"

.PHONY: clean-all
clean-all: clean clean-venv ## Remove everything (venv + cache)
	@echo "$(GREEN)✓ Full cleanup complete$(NC)"

.PHONY: update
update: ## Update all dependencies to latest versions
	@echo "Updating dependencies..."
ifdef UV_AVAILABLE
	@uv pip install --upgrade -r requirements.txt --python $(VENV_PYTHON)
	@echo "$(GREEN)✓ Dependencies updated with uv$(NC)"
else
	@$(VENV_PYTHON) -m pip install --upgrade pip setuptools wheel
	@$(VENV_PYTHON) -m pip install --upgrade -r requirements.txt
	@echo "$(GREEN)✓ Dependencies updated with pip$(NC)"
endif

.PHONY: upgrade-uv
upgrade-uv: ## Upgrade uv to latest version
	@echo "Upgrading uv..."
ifdef UV_AVAILABLE
	@uv self update
	@echo "$(GREEN)✓ uv upgraded to: $$(uv --version)$(NC)"
else
	@echo "$(RED)❌ uv not installed$(NC)"
	@echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
endif

# ============================================================================
# Build and Distribution
# ============================================================================

.PHONY: build
build: clean ## Build distribution packages
	@echo "Building distribution packages..."
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) python -m build
else
	@$(VENV_PYTHON) -m pip install build
	@$(VENV_PYTHON) -m build
endif
	@echo "$(GREEN)✓ Build complete! Check dist/ directory$(NC)"

.PHONY: dist
dist: clean ## Create distribution archive
	@echo "Creating distribution archive..."
	@mkdir -p dist
	tar -czf dist/$(PROJECT_NAME).tar.gz \
		README.md QUICKSTART.md WINDOWS_SETUP.md ENVIRONMENT_SETUP.md \
		agent_langflow.py run.sh run.bat requirements.txt \
		.env.example .gitignore Makefile pyproject.toml setup.cfg
	@echo "$(GREEN)✓ Distribution archive created: dist/$(PROJECT_NAME).tar.gz$(NC)"

# ============================================================================
# Information and Utilities
# ============================================================================

.PHONY: show-env
show-env: ## Show current environment information
	@echo "============================================================================"
	@echo "  Environment Information"
	@echo "============================================================================"
	@echo "Python Version Target: $(PYTHON_VERSION)"
	@echo "Virtual Environment: $(VENV_DIR)"
	@echo ""
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Python Executable: $(VENV_PYTHON)"; \
		echo "Python Version: $$($(VENV_PYTHON) --version 2>&1)"; \
		echo "Pip Version: $$($(VENV_PYTHON) -m pip --version 2>&1)"; \
		echo ""; \
		echo "Package Manager:"; \
		if command -v uv >/dev/null 2>&1; then \
			echo "  uv: $$(uv --version)"; \
		else \
			echo "  uv: not installed"; \
		fi; \
		echo ""; \
		echo "Installed Packages:"; \
		$(VENV_PYTHON) -m pip list 2>/dev/null | head -20; \
	else \
		echo "$(YELLOW)Virtual environment not created yet.$(NC)"; \
		echo "Run: make install"; \
	fi
	@echo ""
	@echo "Environment File:"
	@if [ -f .env ]; then \
		echo "  $(GREEN)✓ .env exists$(NC)"; \
	else \
		echo "  $(RED)✗ .env not found (run: make setup)$(NC)"; \
	fi

.PHONY: version
version: ## Show version information
	@echo "============================================================================"
	@echo "  Version Information"
	@echo "============================================================================"
	@echo "System Python:"
	@python --version 2>&1 || python3 --version 2>&1 || echo "Not found"
	@echo ""
	@if command -v uv >/dev/null 2>&1; then \
		echo "UV Package Manager:"; \
		uv --version; \
	else \
		echo "UV: Not installed"; \
		echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
	fi
	@echo ""
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Virtual Environment Python:"; \
		$(VENV_PYTHON) --version; \
		echo ""; \
		echo "Key Packages:"; \
		$(VENV_PYTHON) -m pip show langflow 2>/dev/null | grep "Name\|Version" || echo "  langflow: Not installed"; \
		$(VENV_PYTHON) -m pip show langchain-ibm 2>/dev/null | grep "Name\|Version" || echo "  langchain-ibm: Not installed"; \
	else \
		echo "Virtual environment not created yet."; \
		echo "Run: make install"; \
	fi

.PHONY: list-packages
list-packages: ## List all installed packages
	@echo "Installed packages:"
	@if [ -d "$(VENV_DIR)" ]; then \
		$(VENV_PYTHON) -m pip list; \
	else \
		echo "$(YELLOW)Virtual environment not created yet.$(NC)"; \
		echo "Run: make install"; \
	fi

.PHONY: outdated
outdated: ## Show outdated packages
	@echo "Checking for outdated packages..."
ifdef UV_AVAILABLE
	@uv pip list --outdated --python $(VENV_PYTHON) 2>/dev/null || \
		$(VENV_PYTHON) -m pip list --outdated
else
	@$(VENV_PYTHON) -m pip list --outdated
endif

# ============================================================================
# Quick Commands
# ============================================================================

.PHONY: quick-start
quick-start: install setup demo ## Quick start: install, setup, and run demo
	@echo "$(GREEN)✅ Quick start complete!$(NC)"

.PHONY: dev-setup
dev-setup: dev setup ## Developer setup: install dev deps and setup env
	@echo "$(GREEN)✅ Development environment ready!$(NC)"

.PHONY: full-setup
full-setup: all setup ## Full setup: install everything including jupyter
	@echo "$(GREEN)✅ Full environment ready!$(NC)"

# ============================================================================
# CI/CD Helpers
# ============================================================================

.PHONY: ci-install
ci-install: ## CI: Install dependencies (uv preferred)
	@echo "Installing for CI environment..."
ifdef UV_AVAILABLE
	@uv venv --python $(PYTHON_VERSION) $(VENV_DIR)
	@uv pip install -e ".[dev]" --python $(VENV_PYTHON)
else
	@$(PYTHON) -m venv $(VENV_DIR)
	@$(VENV_PYTHON) -m pip install --upgrade pip setuptools wheel
	@$(VENV_PYTHON) -m pip install -e ".[dev]"
endif

.PHONY: ci-test
ci-test: ## CI: Run tests with coverage
ifdef UV_AVAILABLE
	@uv run --python $(VENV_PYTHON) pytest tests/ -v --cov=$(PROJECT_NAME) --cov-report=xml
else
	@$(VENV_PYTHON) -m pytest tests/ -v --cov=$(PROJECT_NAME) --cov-report=xml
endif

# ============================================================================
# Default target
# ============================================================================

.DEFAULT_GOAL := help