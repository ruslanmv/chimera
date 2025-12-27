# ============================================================================
# Chimera Desktop Assistant - Makefile
# ============================================================================
# Professional enterprise build system for development and CI/CD
# ============================================================================

.PHONY: help install install-dev install-ollama run dev serve launch stop test test-backend test-frontend test-all clean lint format check security

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# ----------------------------------------------------------------------------
# Help
# ----------------------------------------------------------------------------

help: ## Show this help message
	@echo "$(BLUE)╔════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║           Chimera Desktop Assistant - Make Targets           ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Setup & Installation:$(NC)"
	@grep -E '^install.*:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@grep -E '^(run|dev|serve|launch|stop):.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@grep -E '^test.*:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Code Quality:$(NC)"
	@grep -E '^(lint|format|check|security):.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Cleanup:$(NC)"
	@grep -E '^clean.*:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)Quick Start:$(NC)"
	@echo "  1. make install        # Install all dependencies"
	@echo "  2. make install-ollama # Setup local Ollama (recommended)"
	@echo "  3. make dev            # Start development servers"
	@echo "  4. make test           # Run all tests"
	@echo ""

# ----------------------------------------------------------------------------
# Installation
# ----------------------------------------------------------------------------

install: ## Install all dependencies (Python + Node.js)
	@echo "$(BLUE)📦 Installing Chimera dependencies...$(NC)"
	@echo ""
	@echo "$(GREEN)→ Installing uv (Python package manager)...$(NC)"
	@command -v uv >/dev/null 2>&1 || (curl -LsSf https://astral.sh/uv/install.sh | sh && export PATH="$$HOME/.cargo/bin:$$PATH")
	@echo "$(GREEN)✓ uv installed$(NC)"
	@echo ""
	@echo "$(GREEN)→ Installing Python dependencies...$(NC)"
	uv sync
	@echo "$(GREEN)✓ Python dependencies installed$(NC)"
	@echo ""
	@echo "$(GREEN)→ Installing Node.js dependencies...$(NC)"
	cd frontend && npm install
	@echo "$(GREEN)✓ Node.js dependencies installed$(NC)"
	@echo ""
	@echo "$(GREEN)✓ Installation complete!$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  • Run 'make install-ollama' to setup local LLM (recommended)"
	@echo "  • Run 'make dev' to start development servers"
	@echo ""

install-dev: ## Install all dependencies including dev tools
	@echo "$(BLUE)📦 Installing Chimera with dev dependencies...$(NC)"
	@echo ""
	uv sync --dev
	cd frontend && npm install
	@echo ""
	@echo "$(GREEN)→ Installing Playwright browsers...$(NC)"
	cd frontend && npx playwright install --with-deps chromium
	@echo "$(GREEN)✓ Dev installation complete!$(NC)"
	@echo ""

install-ollama: ## Install and setup Ollama with default model
	@echo "$(BLUE)🧠 Setting up Ollama for local LLM...$(NC)"
	@echo ""
	@chmod +x scripts/setup_ollama.sh
	@./scripts/setup_ollama.sh
	@echo ""
	@echo "$(GREEN)✓ Ollama setup complete!$(NC)"
	@echo ""
	@echo "$(YELLOW)To use Ollama:$(NC)"
	@echo "  • Set CHIMERA_DEFAULT_PROVIDER=ollama in .env"
	@echo "  • No API keys required!"
	@echo ""

# ----------------------------------------------------------------------------
# Development
# ----------------------------------------------------------------------------

run: ## Run backend server only
	@echo "$(BLUE)🚀 Starting Chimera backend...$(NC)"
	@echo ""
	uv run chimera-serve

dev: ## Start both backend and frontend in development mode
	@echo "$(BLUE)🚀 Starting Chimera in development mode...$(NC)"
	@echo ""
	@echo "$(YELLOW)Starting backend server...$(NC)"
	@echo "Backend will run on: http://localhost:8000"
	@echo ""
	@echo "$(YELLOW)Starting frontend server...$(NC)"
	@echo "Frontend will run on: http://localhost:5173"
	@echo ""
	@echo "$(GREEN)Press Ctrl+C to stop both servers$(NC)"
	@echo ""
	@trap 'kill 0' EXIT; \
	(cd frontend && npm run dev) & \
	uv run chimera-serve

serve: dev ## Alias for 'make dev'

launch: ## Launch Chimera as a desktop application using Eel
	@echo "$(BLUE)🚀 Launching Chimera Desktop Application...$(NC)"
	@echo ""
	@echo "$(YELLOW)Building frontend...$(NC)"
	@cd frontend && npm run build
	@echo ""
	@echo "$(GREEN)✓ Frontend built$(NC)"
	@echo ""
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	@uv sync
	@echo ""
	@echo "$(GREEN)Starting desktop application...$(NC)"
	@echo ""
	@uv run chimera-launch

stop: ## Stop all running Chimera servers
	@echo "$(BLUE)🛑 Stopping Chimera servers...$(NC)"
	@echo ""
	@echo "$(YELLOW)→ Killing backend processes...$(NC)"
	@pkill -f "uvicorn.*chimera" 2>/dev/null && echo "$(GREEN)  ✓ Backend stopped$(NC)" || echo "$(YELLOW)  ℹ️  No backend process found$(NC)"
	@pkill -f "chimera-serve" 2>/dev/null && echo "$(GREEN)  ✓ Chimera-serve stopped$(NC)" || echo "$(YELLOW)  ℹ️  No chimera-serve process found$(NC)"
	@echo ""
	@echo "$(YELLOW)→ Killing frontend processes...$(NC)"
	@pkill -f "vite.*5173" 2>/dev/null && echo "$(GREEN)  ✓ Frontend stopped$(NC)" || echo "$(YELLOW)  ℹ️  No frontend process found$(NC)"
	@pkill -f "node.*vite" 2>/dev/null || true
	@echo ""
	@echo "$(YELLOW)→ Checking for any remaining processes...$(NC)"
	@lsof -ti:8000 2>/dev/null | xargs kill -9 2>/dev/null && echo "$(GREEN)  ✓ Port 8000 freed$(NC)" || echo "$(YELLOW)  ℹ️  Port 8000 already free$(NC)"
	@lsof -ti:5173 2>/dev/null | xargs kill -9 2>/dev/null && echo "$(GREEN)  ✓ Port 5173 freed$(NC)" || echo "$(YELLOW)  ℹ️  Port 5173 already free$(NC)"
	@echo ""
	@echo "$(GREEN)✓ All servers stopped!$(NC)"
	@echo "$(YELLOW)Tip: Run 'make dev' to start servers again$(NC)"
	@echo ""

# ----------------------------------------------------------------------------
# Testing
# ----------------------------------------------------------------------------

test: test-backend ## Run all tests (backend + frontend)

test-backend: ## Run Python backend tests
	@echo "$(BLUE)🧪 Running Python backend tests...$(NC)"
	@echo ""
	@if ! command -v ollama >/dev/null 2>&1; then \
		echo "$(YELLOW)⚠️  Ollama not found. Tests will run without Ollama integration tests.$(NC)"; \
	else \
		echo "$(GREEN)→ Checking Ollama server...$(NC)"; \
		if ! curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then \
			echo "$(YELLOW)→ Starting Ollama server...$(NC)"; \
			ollama serve > /tmp/ollama.log 2>&1 & \
			sleep 3; \
		fi; \
		echo "$(GREEN)→ Checking test model...$(NC)"; \
		if ! ollama list | grep -q "gemma:2b"; then \
			echo "$(YELLOW)→ Pulling test model (gemma:2b)...$(NC)"; \
			ollama pull gemma:2b; \
		fi; \
	fi
	@echo "$(GREEN)→ Running pytest...$(NC)"
	@CHIMERA_DEFAULT_PROVIDER=ollama \
	OLLAMA_BASE_URL=http://127.0.0.1:11434 \
	OLLAMA_MODEL=gemma:2b \
	uv run pytest tests/ -v --tb=short
	@echo ""
	@echo "$(GREEN)✓ Backend tests complete!$(NC)"

test-launch: ## Test the Eel launcher functionality
	@echo "$(BLUE)🧪 Testing Eel launcher...$(NC)"
	@echo ""
	@echo "$(GREEN)→ Running launcher tests...$(NC)"
	@uv run pytest tests/test_eel_launcher.py -v --tb=short
	@echo ""
	@echo "$(GREEN)✓ Launcher tests complete!$(NC)"

test-frontend: ## Run Playwright UI tests
	@echo "$(BLUE)🧪 Running Playwright UI tests...$(NC)"
	@echo ""
	@echo "$(GREEN)→ Building frontend...$(NC)"
	cd frontend && npm run build
	@echo "$(GREEN)→ Running Playwright tests...$(NC)"
	cd frontend && npx playwright test
	@echo ""
	@echo "$(GREEN)✓ Frontend tests complete!$(NC)"

test-all: install-dev test ## Install dev dependencies and run all tests

test-coverage: ## Run tests with coverage report
	@echo "$(BLUE)📊 Running tests with coverage...$(NC)"
	@CHIMERA_DEFAULT_PROVIDER=ollama \
	OLLAMA_BASE_URL=http://127.0.0.1:11434 \
	OLLAMA_MODEL=gemma:2b \
	uv run pytest tests/ -v --cov=backend --cov-report=html --cov-report=term
	@echo ""
	@echo "$(GREEN)✓ Coverage report generated: htmlcov/index.html$(NC)"

# ----------------------------------------------------------------------------
# Code Quality
# ----------------------------------------------------------------------------

lint: ## Run linters (ruff + eslint)
	@echo "$(BLUE)🔍 Running linters...$(NC)"
	@echo ""
	@echo "$(GREEN)→ Running ruff (Python)...$(NC)"
	uv run ruff check backend/ tests/ || true
	@echo ""
	@echo "$(GREEN)→ Running eslint (JavaScript/React)...$(NC)"
	cd frontend && npm run lint || true
	@echo ""
	@echo "$(GREEN)✓ Linting complete!$(NC)"

format: ## Format code (black + prettier)
	@echo "$(BLUE)✨ Formatting code...$(NC)"
	@echo ""
	@echo "$(GREEN)→ Running black (Python)...$(NC)"
	uv run black backend/ tests/ || true
	@echo ""
	@echo "$(GREEN)→ Running prettier (JavaScript/React)...$(NC)"
	cd frontend && npm run format || npx prettier --write src/ || true
	@echo ""
	@echo "$(GREEN)✓ Code formatted!$(NC)"

check: lint test ## Run linters and tests (CI check)
	@echo ""
	@echo "$(GREEN)✓ All checks passed!$(NC)"

security: ## Run security vulnerability scan
	@echo "$(BLUE)🔒 Running security scan...$(NC)"
	@echo ""
	@command -v trivy >/dev/null 2>&1 || (echo "$(YELLOW)Installing Trivy...$(NC)" && \
		curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin)
	trivy fs . --severity HIGH,CRITICAL || true
	@echo ""
	@echo "$(GREEN)✓ Security scan complete!$(NC)"

# ----------------------------------------------------------------------------
# Cleanup
# ----------------------------------------------------------------------------

clean: ## Remove build artifacts and caches
	@echo "$(BLUE)🧹 Cleaning build artifacts...$(NC)"
	@echo ""
	@echo "$(GREEN)→ Removing Python caches...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)→ Removing test artifacts...$(NC)"
	rm -rf .pytest_cache htmlcov .coverage 2>/dev/null || true
	rm -rf frontend/test-results frontend/playwright-report 2>/dev/null || true
	@echo "$(GREEN)→ Removing build directories...$(NC)"
	rm -rf frontend/dist frontend/build 2>/dev/null || true
	rm -rf backend/static/*.png backend/static/*.jpg 2>/dev/null || true
	@echo ""
	@echo "$(GREEN)✓ Cleanup complete!$(NC)"

clean-all: clean ## Remove all dependencies and caches
	@echo "$(BLUE)🧹 Deep cleaning...$(NC)"
	@echo ""
	rm -rf .venv node_modules frontend/node_modules 2>/dev/null || true
	@echo "$(GREEN)✓ Deep cleanup complete!$(NC)"
	@echo "$(YELLOW)Run 'make install' to reinstall dependencies$(NC)"

# ----------------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------------

health: ## Check system health and dependencies
	@echo "$(BLUE)🏥 Chimera Health Check$(NC)"
	@echo ""
	@echo "$(GREEN)Python:$(NC)"
	@python3 --version || echo "$(RED)✗ Python not found$(NC)"
	@echo ""
	@echo "$(GREEN)uv:$(NC)"
	@uv --version || echo "$(RED)✗ uv not found (run: make install)$(NC)"
	@echo ""
	@echo "$(GREEN)Node.js:$(NC)"
	@node --version || echo "$(RED)✗ Node.js not found$(NC)"
	@echo ""
	@echo "$(GREEN)npm:$(NC)"
	@npm --version || echo "$(RED)✗ npm not found$(NC)"
	@echo ""
	@echo "$(GREEN)Ollama:$(NC)"
	@ollama --version || echo "$(YELLOW)⚠️  Ollama not found (optional, run: make install-ollama)$(NC)"
	@echo ""
	@echo "$(GREEN)Backend Server:$(NC)"
	@curl -s http://localhost:8000/api/health >/dev/null 2>&1 && echo "$(GREEN)✓ Running on http://localhost:8000$(NC)" || echo "$(YELLOW)⚠️  Not running (run: make dev)$(NC)"
	@echo ""
	@echo "$(GREEN)Frontend Server:$(NC)"
	@curl -s http://localhost:5173 >/dev/null 2>&1 && echo "$(GREEN)✓ Running on http://localhost:5173$(NC)" || echo "$(YELLOW)⚠️  Not running (run: make dev)$(NC)"
	@echo ""

status: health ## Alias for 'make health'

.PHONY: help install install-dev install-ollama run dev serve stop test test-backend test-frontend test-all test-coverage lint format check security clean clean-all health status
