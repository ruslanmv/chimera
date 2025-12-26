# Chimera Test Suite

Comprehensive tests for multimodal UE5 assistant functionality and provider integrations.

## Test Files

### `test_chimera.py` - Core Component Tests
- Basic installation verification
- Plugin imports and discovery
- API endpoint structure
- MCP server functionality
- Multi-provider integration
- Configuration management

### `test_vision_providers.py` - Vision API Tests
- **OpenAI GPT-4o Vision** (Official API ✅)
- **Anthropic Claude Vision** (Official API ✅)
- **Google Gemini Vision** (Official API ✅)
- **Ollama LLaVA** (Local model ✅)
- Multi-provider comparison
- Error handling and retries
- Response structure validation

### `test_ue5_assistance.py` - UE5-Specific Tests
- Blueprint guidance formatting
- Material editor assistance
- Landscape tool guidance
- Step-by-step response validation
- Context awareness

## Running Tests

### All Tests
```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v -s
```

### Provider-Specific Tests
```bash
# Only vision provider tests
uv run pytest -m vision -v -s

# Specific provider tests
uv run pytest tests/test_vision_providers.py::TestOpenAIVision -v -s
uv run pytest tests/test_vision_providers.py::TestOllamaVision -v -s
```

### With Coverage
```bash
# Generate coverage report
uv run pytest --cov=backend --cov-report=html

# View report
open htmlcov/index.html
```

## Prerequisites

### 1. Start the Server
```bash
# Terminal 1: Start Chimera
make dev
# or
uv run chimera-serve
```

### 2. Configure Provider Credentials

Create a `.env.test` file for testing:

```bash
# OpenAI (requires API key)
OPENAI_API_KEY=sk-...

# Anthropic (requires API key)
ANTHROPIC_API_KEY=sk-ant-...

# Google Gemini (requires API key)
GOOGLE_API_KEY=...

# Ollama (local - no key needed)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llava:latest
```

**Note:** Tests will skip providers without configured credentials.

### 3. (Optional) Set Up Ollama for Local Tests

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull vision models
ollama pull llava:latest
ollama pull bakllava

# Verify
ollama run llava "Test" < test_image.png
```

## Test Categories

Tests are marked with pytest markers:

| Marker | Description | Command |
|--------|-------------|---------|
| `@pytest.mark.vision` | Vision/multimodal tests | `pytest -m vision` |
| `@pytest.mark.asyncio` | Async tests | Automatically handled |
| `@pytest.mark.integration` | Integration tests | `pytest -m integration` |
| `@pytest.mark.unit` | Unit tests | `pytest -m unit` |

## Example Test Run

```bash
# Start server in one terminal
$ make dev

# In another terminal, run vision tests
$ uv run pytest tests/test_vision_providers.py -v -s

============================= test session starts ==============================
platform linux -- Python 3.11.14, pytest-9.0.2
collected 8 items

tests/test_vision_providers.py::TestServerAvailability::test_server_is_running PASSED
✓ Server is running. Available plugins: ['chimera', 'openai', 'ollama']

tests/test_vision_providers.py::TestOpenAIVision::test_blueprint_analysis PASSED
🤖 OpenAI Vision Test:
  Question: How do I connect these Blueprint nodes?
  Success: True
  Summary: Type mismatch between Vector and Float pins
  Steps: 2

tests/test_vision_providers.py::TestOllamaVision::test_blueprint_analysis PASSED
🤖 Ollama Vision Test:
  Question: How do I connect these Blueprint nodes?
  Success: True
  Summary: Vector to Float conversion needed
  Steps: 2

...
```

## Writing New Tests

### Template for Vision Provider Tests

```python
@pytest.mark.vision
class TestYourProviderVision:
    """Test YourProvider vision capabilities for UE5 assistance"""

    @pytest.mark.asyncio
    async def test_blueprint_analysis(self):
        """Test Blueprint screenshot analysis"""
        async with VisionProviderTester() as tester:
            # Load test image
            image_path = "tests/fixtures/blueprint_error.png"

            # Prepare request
            request = {
                "image": image_path,
                "question": "How do I fix this Blueprint node connection?",
                "context": "ue5-blueprint",
                "ue5_version": "5.3"
            }

            # Query provider
            result = await tester.query_provider("yourprovider", request)

            # Validate response structure
            assert result['success'], "Query should succeed"
            assert 'summary' in result
            assert 'steps' in result
            assert len(result['steps']) > 0

            # Validate step structure
            for step in result['steps']:
                assert 'title' in step
                assert 'details' in step
                assert 'why' in step

            print(f"\n🤖 YourProvider Test:")
            print(f"  Summary: {result['summary']}")
            print(f"  Steps: {len(result['steps'])}")
```

## Test Fixtures

Standard test images in `tests/fixtures/`:

| File | Context | Description |
|------|---------|-------------|
| `blueprint_connection.png` | Blueprint | Node connection type mismatch |
| `material_error.png` | Material | Pink material error |
| `landscape_spikes.png` | Landscape | Terrain smoothing needed |
| `animation_setup.png` | Animation | Blueprint setup |

## Test Questions

Standard test questions for consistent validation:

1. **Blueprint:** "How do I connect these nodes?" (Expected: Type conversion steps)
2. **Material:** "Why is my material pink?" (Expected: Texture/connection checks)
3. **Landscape:** "How do I smooth this terrain?" (Expected: Smooth tool steps)
4. **Animation:** "How do I set up this animation?" (Expected: Blueprint setup)

## Validation Criteria

All vision provider responses must include:

```python
{
    "success": True,
    "summary": "One-line description (required)",
    "assumptions": ["List of assumptions (optional)"],
    "steps": [
        {
            "title": "Step name (required)",
            "details": ["Action 1", "Action 2 (required)"],
            "why": "Explanation (required)"
        }
    ],
    "checks": ["Verification steps (optional)"]
}
```

## Troubleshooting

### Server Not Running
```
Error: Connection refused

Solution: Start the server with 'make dev' or 'uv run chimera-serve'
```

### Missing API Keys
```
Error: OPENAI_API_KEY not found

Solution:
1. Create .env file
2. Add: OPENAI_API_KEY=sk-...
3. Run tests again
```

Tests will automatically skip providers without configured credentials.

### Ollama Not Running
```
Error: Connection refused to localhost:11434

Solution:
1. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh
2. Start Ollama: ollama serve
3. Pull model: ollama pull llava:latest
```

### Timeout Errors
```
Error: Request timeout after 60s

Solution: Vision analysis can be slow. Adjust timeout:
TIMEOUT = 120.0  # Increase to 2 minutes
```

### Rate Limiting
```
Error: Rate limit exceeded

Solution: Add delays between test queries:
await asyncio.sleep(5)  # Wait 5 seconds
```

## CI/CD Integration

For continuous integration:

```bash
# Run only tests that don't require API keys
pytest -m "not vision or local"

# Run with Ollama only (local model)
pytest -m "vision and local"

# Skip integration tests
pytest -m "not integration"
```

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      # Run unit tests (no API keys needed)
      - run: uv run pytest -m unit

      # Run integration tests with Ollama
      - run: |
          curl -fsSL https://ollama.ai/install.sh | sh
          ollama pull llava:latest
          uv run pytest -m "vision and local"
```

## Contributing

When adding a new provider:

1. Implement the provider in `backend/plugins/your_provider.py`
2. Add tests in `test_vision_providers.py`
3. Use the `VisionProviderTester` helper class
4. Include test fixtures (sample images)
5. Test with UE5-specific scenarios
6. Validate response structure

## Coverage Goals

Target coverage by component:

- Core components: 80%+
- Vision providers: 70%+
- API endpoints: 90%+
- MCP server: 70%+
- UE5 assistance: 75%+

Check current coverage:
```bash
uv run pytest --cov=backend --cov-report=term
```

## Performance Benchmarks

Track provider performance:

```bash
# Run benchmark tests
uv run pytest tests/test_benchmarks.py -v

# Expected metrics:
# - Response time: < 10s for most queries
# - Step quality: >= 2 actionable steps
# - Accuracy: Manual validation of top 10 queries
```

## Support

- 🐛 Report test failures: [GitHub Issues](https://github.com/ruslanmv/chimera/issues)
- 💬 Test discussions: [GitHub Discussions](https://github.com/ruslanmv/chimera/discussions)
- 📖 More info: See main README.md

---

**Important:** All tests use official APIs or local models. No unauthorized service access is tested or supported.
