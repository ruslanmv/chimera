# Chimera Plugins - README

## 🔌 LLM Provider Plugins

**Chimera's plugin architecture allows integration with multiple AI providers for multimodal UE5 assistance.**

### Available Plugins

#### 🌐 Chimera Server (Default)
- **`chimera_server.py`** - Managed hosting, no configuration required
- **Status:** ✅ Working
- **Setup:** None - works out of the box
- **Privacy:** Enterprise-grade, screenshots not stored

#### 🔑 Official API Plugins
- **`openai.py`** - OpenAI GPT-4o with Vision (requires `OPENAI_API_KEY`)
- **`claude.py`** - Anthropic Claude 3.5 Sonnet (requires `ANTHROPIC_API_KEY`)
- **`gemini.py`** - Google Gemini Pro Vision (requires `GOOGLE_API_KEY`)
- **`watsonx.py`** - IBM WatsonX API (requires `WATSONX_API_KEY` + `WATSONX_PROJECT_ID`)

#### 💻 Local Models
- **`ollama.py`** ✅ Working - Local multimodal models (LLaVA, Bakllava, etc.)
  - 100% private and free
  - No API key required
  - Requires Ollama installation

---

## How Plugins Work

### Official API Plugin Structure

```python
from backend.core.plugin_base import BaseLLMHead
from openai import AsyncOpenAI

class OpenAIHead(BaseLLMHead):
    plugin_name = "openai"

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key required")
        self.client = AsyncOpenAI(api_key=api_key)

    async def vision_chat_completion(self, request):
        # Direct API call with image + text
        # Returns structured response with steps
```

### Local Model Plugin Structure

```python
from backend.core.plugin_base import BaseLLMHead
import ollama

class OllamaHead(BaseLLMHead):
    plugin_name = "ollama"

    def __init__(self):
        self.model = os.getenv("OLLAMA_MODEL", "llava:latest")
        # Verify Ollama is running

    async def vision_chat_completion(self, request):
        # Call local Ollama instance
        # Process multimodal input
        # Return structured steps
```

---

## Contributing a New Provider

Want to add support for a new LLM provider with vision capabilities? Here's how:

### 1. Check Provider Requirements

Ensure the provider supports:
- ✅ Vision/image input (for screenshot analysis)
- ✅ Structured output or JSON mode (for step-by-step responses)
- ✅ Official API or local deployment

### 2. Create `your_provider.py`

```python
from backend.core.plugin_base import BaseLLMHead
from typing import Dict, Any
import os

class YourProviderHead(BaseLLMHead):
    plugin_name = "yourprovider"

    def __init__(self):
        # Initialize API client
        api_key = os.getenv("YOURPROVIDER_API_KEY")
        if not api_key:
            raise ValueError("YOURPROVIDER_API_KEY required")
        self.client = YourProviderClient(api_key=api_key)

    async def vision_chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process multimodal request with image + question

        Args:
            request: {
                "image": base64_encoded_image,
                "question": "How do I fix this?",
                "context": "ue5-blueprint",
                "ue5_version": "5.3"
            }

        Returns:
            {
                "summary": "Brief issue description",
                "steps": [
                    {
                        "title": "Step name",
                        "details": ["Action 1", "Action 2"],
                        "why": "Explanation"
                    }
                ],
                "checks": ["Verification step 1", ...]
            }
        """
        # 1. Prepare image + prompt
        # 2. Call provider API
        # 3. Parse response into structured format
        # 4. Return step-by-step guidance

        return {
            "summary": "Parsed from AI response",
            "steps": [...],
            "checks": [...]
        }
```

### 3. Add Configuration

Update `.env.example`:
```bash
# Your Provider
YOURPROVIDER_API_KEY=your-api-key-here
YOURPROVIDER_MODEL=yourprovider-vision-v1  # Optional model selection
```

### 4. Register Plugin

The plugin will be auto-discovered by the Chimera Manager. Ensure:
- File is in `backend/plugins/` directory
- Class inherits from `BaseLLMHead`
- Has a unique `plugin_name` attribute

### 5. Test It

```bash
# Set your API key
export YOURPROVIDER_API_KEY=your-key

# Test the plugin
uv run pytest tests/test_plugins.py::TestYourProvider -v
```

### 6. Submit a PR

Include:
- Plugin implementation (`your_provider.py`)
- Tests (`tests/test_your_provider.py`)
- Documentation updates
- Example usage

---

## Plugin Priority System

When a request comes in, Chimera routes to the configured provider:

1. **Check `CHIMERA_DEFAULT_PROVIDER` env var** - Use specified provider
2. **Fall back to Chimera Server** - If no provider configured
3. **Error if provider unavailable** - Return helpful error message

Configure in `.env`:
```bash
CHIMERA_DEFAULT_PROVIDER=openai  # or anthropic, google, ollama, chimera
```

---

## Provider Comparison

| Provider | Vision? | Setup | Cost | Privacy | Best For |
|----------|---------|-------|------|---------|----------|
| **Chimera Server** | ✅ | None | Included | Enterprise | Most users |
| **OpenAI** | ✅ | API key | Pay-per-use | Sent to OpenAI | Highest quality |
| **Anthropic** | ✅ | API key | Pay-per-use | Sent to Anthropic | Strong reasoning |
| **Google Gemini** | ✅ | API key | Pay-per-use | Sent to Google | Fast responses |
| **Ollama** | ✅ | Install | Free | 100% local | Privacy-focused |

---

## Best Practices

### Error Handling

```python
async def vision_chat_completion(self, request):
    try:
        response = await self.client.chat(...)
        return self.parse_response(response)
    except ProviderAPIError as e:
        raise ChimeraError(f"{self.plugin_name} API error: {str(e)}")
    except Exception as e:
        raise ChimeraError(f"Unexpected error in {self.plugin_name}: {str(e)}")
```

### Response Formatting

Always return structured responses for UE5 guidance:
```python
{
    "summary": "One-line issue description",
    "assumptions": ["UE5.3", "Blueprint Editor open"],
    "steps": [
        {
            "title": "Action to take",
            "details": ["Specific instruction 1", "Specific instruction 2"],
            "why": "Explanation of why this helps"
        }
    ],
    "checks": ["Verification step to ensure success"]
}
```

### API Key Security

- Never hardcode API keys
- Use environment variables
- Validate keys exist before use
- Provide clear error messages if missing

---

## Community Contributions Needed

We're looking for help with:

- 🔌 **More Provider Integrations** - Mistral, Cohere, DeepSeek (official APIs)
- 🎮 **UE5-Specific Tuning** - Better prompts for Blueprint/Material/Landscape contexts
- 🧪 **Testing** - Comprehensive test coverage for all providers
- 📝 **Documentation** - Better examples and guides

---

## Support

- 🐛 Report issues: [GitHub Issues](https://github.com/ruslanmv/chimera/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/ruslanmv/chimera/discussions)
- 📖 Docs: See main README.md

---

**Note:** All plugins must use official APIs or local models. We do not support unauthorized access to third-party services.
