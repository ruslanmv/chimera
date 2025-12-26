# Chimera Testing Guide

Comprehensive testing infrastructure for the Chimera Desktop Assistant enterprise project.

## Table of Contents

- [Overview](#overview)
- [Test Infrastructure](#test-infrastructure)
- [Running Tests Locally](#running-tests-locally)
- [CI/CD Pipeline](#cicd-pipeline)
- [Writing Tests](#writing-tests)
- [Troubleshooting](#troubleshooting)

## Overview

Chimera uses a multi-layered testing approach:

1. **Python Unit Tests** - Backend logic and LLM provider integration
2. **UI Tests** - Playwright-based visual regression testing
3. **Integration Tests** - End-to-end workflow validation
4. **Security Scanning** - Trivy vulnerability scanning

All tests run automatically on every push and pull request via GitHub Actions.

## Test Infrastructure

### Backend Testing

```bash
# Python test framework
- pytest for unit tests
- pytest-asyncio for async tests
- pytest-cov for coverage reporting

# Test directory structure
tests/
├── test_settings.py          # Settings validation
├── test_llm_provider.py      # LLM provider abstraction
├── test_model_catalog.py     # Model discovery
└── test_vision_api.py        # Vision endpoint tests
```

### Frontend Testing

```bash
# UI test framework
- Playwright for browser automation
- TypeScript for type safety
- Screenshot regression testing

# Test directory structure
frontend/tests/
├── ui.spec.ts                # Main UI tests
└── playwright.config.ts      # Playwright configuration
```

## Running Tests Locally

### Prerequisites

```bash
# Install Python dependencies
uv sync --dev

# Install Node.js dependencies
cd frontend && npm install

# Install Playwright browsers
cd frontend && npx playwright install --with-deps chromium

# Setup Ollama for testing (optional but recommended)
./scripts/setup_ollama.sh gemma:2b
```

### Run Python Tests

```bash
# Run all Python tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ -v --cov=backend --cov-report=html

# Run specific test file
uv run pytest tests/test_llm_provider.py -v

# Run with environment variables
CHIMERA_DEFAULT_PROVIDER=ollama \
OLLAMA_MODEL=gemma:2b \
uv run pytest tests/ -v
```

### Run UI Tests

```bash
# Start backend server (in terminal 1)
uv run chimera-serve

# Start frontend dev server (in terminal 2)
cd frontend && npm run dev

# Run Playwright tests (in terminal 3)
cd frontend && npx playwright test

# Run tests in UI mode (interactive)
cd frontend && npx playwright test --ui

# Run specific test
cd frontend && npx playwright test ui.spec.ts

# Generate test report
cd frontend && npx playwright show-report
```

### Run All Tests (Full Suite)

```bash
# Use Make for complete test suite
make test

# Or run manually
./scripts/run_all_tests.sh
```

## CI/CD Pipeline

### GitHub Actions Workflow

File: `.github/workflows/ci-test.yml`

The CI pipeline runs on:
- Push to `main`, `dev`, or `claude/*` branches
- Pull requests to `main` or `dev`
- Manual workflow dispatch

### Pipeline Stages

#### 1. Test Job (Matrix Strategy)

Runs on multiple Python/Node versions:
- Python: 3.11, 3.12
- Node.js: 20

```yaml
Steps:
1. Checkout code
2. Setup Python & Node.js
3. Install uv package manager
4. Install & start Ollama
5. Pull test model (gemma:2b)
6. Install Python dependencies
7. Install frontend dependencies
8. Run Python unit tests
9. Start backend server
10. Build frontend
11. Start frontend dev server
12. Install Playwright
13. Run UI screenshot tests
14. Upload test artifacts
15. Cleanup processes
16. Publish test results
```

#### 2. Lint Job

Code quality checks:
- Python: ruff (linting) + black (formatting)
- Frontend: eslint

#### 3. Security Job

Vulnerability scanning with Trivy:
- Scans filesystem for vulnerabilities
- Uploads SARIF results to GitHub Security

### Environment Variables for CI

```bash
# Backend tests
CHIMERA_DEFAULT_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=gemma:2b

# Frontend tests
CI=true
```

### Test Artifacts

After each CI run, the following artifacts are available:

1. **UI Screenshots** - Visual regression screenshots
2. **Test Results** - JUnit XML reports
3. **Coverage Reports** - Python code coverage
4. **Security Scan Results** - SARIF vulnerability reports

Artifacts are retained for 7 days.

## Writing Tests

### Python Unit Test Example

```python
# tests/test_llm_provider.py
import pytest
from backend.core.llm_provider import build_llm, LLMProviderError
from backend.core.settings import AppSettings, LLMProvider

def test_build_ollama_llm():
    """Test building Ollama LLM provider"""
    settings = AppSettings(provider=LLMProvider.ollama)
    llm = build_llm(settings)

    assert llm is not None
    assert "ollama/" in llm.model

def test_missing_api_key_raises_error():
    """Test that missing API keys raise appropriate errors"""
    settings = AppSettings(
        provider=LLMProvider.openai,
        openai={"api_key": None}
    )

    with pytest.raises(LLMProviderError):
        build_llm(settings)
```

### Playwright UI Test Example

```typescript
// frontend/tests/ui.spec.ts
import { test, expect } from '@playwright/test';

test('should load Chimera launcher', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // Verify heading
  const heading = page.locator('h1:has-text("CHIMERA")');
  await expect(heading).toBeVisible();

  // Take screenshot
  await page.screenshot({
    path: 'test-results/screenshots/launcher.png',
    fullPage: true
  });
});

test('should toggle monitoring state', async ({ page }) => {
  await page.goto('/');

  const startButton = page.locator('button:has-text("Start Monitoring")');
  await startButton.click();

  // Verify green border appears
  const border = page.locator('.border-green-500');
  await expect(border).toBeVisible();

  await page.screenshot({
    path: 'test-results/screenshots/monitoring.png'
  });
});
```

### Integration Test Example

```python
# tests/test_integration.py
import pytest
import httpx
from PIL import Image
import io

@pytest.mark.asyncio
async def test_vision_endpoint_integration():
    """Test complete vision analysis workflow"""
    async with httpx.AsyncClient() as client:
        # Create test image
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        # Upload to vision endpoint
        response = await client.post(
            "http://localhost:8000/api/vision",
            data={
                "model": "ollama",
                "prompt": "Describe this image"
            },
            files={"file": ("test.png", img_bytes, "image/png")}
        )

        assert response.status_code == 200
        assert "response" in response.json()
```

## Test Coverage Goals

We aim for the following coverage targets:

- **Backend Core**: 80%+ coverage
- **LLM Providers**: 90%+ coverage
- **API Endpoints**: 85%+ coverage
- **UI Components**: 70%+ coverage

View coverage reports:

```bash
# Python coverage
uv run pytest tests/ --cov=backend --cov-report=html
open htmlcov/index.html

# Frontend coverage (if configured)
cd frontend && npm run test:coverage
```

## Troubleshooting

### Common Issues

#### 1. Ollama Not Starting in CI

**Problem**: `Ollama API did not become ready in time`

**Solution**: The CI workflow has retry logic, but if issues persist:
```yaml
# Increase timeout in .github/workflows/ci-test.yml
for i in {1..60}; do  # Changed from 30 to 60
```

#### 2. Playwright Browser Installation Failed

**Problem**: `browserType.launch: Executable doesn't exist`

**Solution**:
```bash
cd frontend
npx playwright install --with-deps chromium
```

#### 3. Backend Health Check Fails

**Problem**: `Connection refused on http://localhost:8000/api/health`

**Solution**: Ensure backend is running:
```bash
# Check if backend is running
curl http://localhost:8000/api/health

# Start backend if not running
uv run chimera-serve
```

#### 4. Screenshot Diffs in CI

**Problem**: Screenshots differ between local and CI

**Solution**: Use `toMatchSnapshot()` with threshold:
```typescript
await expect(page).toHaveScreenshot({
  maxDiffPixels: 100,
  threshold: 0.2
});
```

#### 5. Test Model Download Slow

**Problem**: `ollama pull` taking too long in CI

**Solution**: Use smallest viable model:
```bash
# In CI workflow, use gemma:2b instead of larger models
ollama pull gemma:2b  # ~1.7GB instead of 7GB+
```

### Debug Mode

Run tests with debug output:

```bash
# Python tests
uv run pytest tests/ -v -s --log-cli-level=DEBUG

# Playwright tests (headed mode)
cd frontend && npx playwright test --headed --debug

# Playwright with trace
cd frontend && npx playwright test --trace on
```

### CI Debug

Enable CI debug logging:

```bash
# Add to workflow file
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

## Performance Benchmarks

Expected test execution times:

| Test Suite | Local | CI (GitHub Actions) |
|------------|-------|---------------------|
| Python Unit Tests | 5-10s | 10-20s |
| UI Tests (Playwright) | 30-60s | 60-120s |
| Full CI Pipeline | - | 5-8 minutes |
| Ollama Model Pull | 60-120s | 120-180s |

## Contributing

When adding new features:

1. ✅ Write tests FIRST (TDD approach)
2. ✅ Ensure tests pass locally
3. ✅ Add integration tests for new endpoints
4. ✅ Update screenshot baselines if UI changed
5. ✅ Run full test suite before PR: `make test`

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)

---

**Last Updated**: 2025-12-26
**Maintained by**: Chimera Development Team
