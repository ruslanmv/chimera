# Chimera Configuration Guide

Complete guide to configuring the Chimera Desktop Assistant for development and production environments.

## Table of Contents

- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [Provider Configuration](#provider-configuration)
- [Multi-Monitor Setup](#multi-monitor-setup)
- [Privacy Settings](#privacy-settings)
- [Production Deployment](#production-deployment)

## Quick Start

### 1. Copy Environment Template

```bash
cp .env.example .env
```

### 2. Choose Your Provider

For local development (recommended):
```bash
# Edit .env
CHIMERA_DEFAULT_PROVIDER=ollama

# Setup Ollama
./scripts/setup_ollama.sh
```

For production with OpenAI:
```bash
# Edit .env
CHIMERA_DEFAULT_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
```

### 3. Start Chimera

```bash
make dev
```

Visit: http://localhost:5173

## Environment Variables

### General Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `"Chimera Desktop Assistant"` | Application name |
| `DEBUG` | `false` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `CHIMERA_DEFAULT_PROVIDER` | `chimera` | Active LLM provider |

### Server Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `127.0.0.1` | Server bind address |
| `PORT` | `8000` | Server port |
| `RELOAD` | `false` | Enable auto-reload on code changes |

### Feature Flags

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_MONITORING` | `true` | Enable screen monitoring features |
| `ENABLE_MULTI_MONITOR` | `true` | Enable multi-monitor support |

### Privacy Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `STORE_SCREENSHOTS` | `false` | Store screenshots on server (not recommended) |
| `ANALYTICS_ENABLED` | `false` | Enable usage analytics |

## Provider Configuration

### Chimera Server (Managed Hosting)

**Best for**: Production deployments, teams, easiest setup

```bash
CHIMERA_DEFAULT_PROVIDER=chimera
CHIMERA_SERVER_API_URL=https://api.chimera-ai.com/v1
CHIMERA_SERVER_API_KEY=your-api-key-here
CHIMERA_SERVER_MODEL=chimera-vision-1
```

**Setup Steps**:
1. Sign up at https://chimera-ai.com/signup
2. Copy your API key from dashboard
3. Set environment variables
4. Start Chimera

**Features**:
- ✅ Multimodal vision support
- ✅ Managed infrastructure
- ✅ Free tier available (100 requests/day)
- ✅ No local GPU required

### OpenAI

**Best for**: Best-in-class vision quality, production use

```bash
CHIMERA_DEFAULT_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
OPENAI_BASE_URL=  # Optional: custom endpoint
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2048
```

**Setup Steps**:
1. Get API key: https://platform.openai.com/api-keys
2. Set `OPENAI_API_KEY` in `.env`
3. Choose model: `gpt-4o` (best), `gpt-4o-mini` (cost-effective)
4. Start Chimera

**Recommended Models**:
- `gpt-4o` - Best vision and reasoning
- `gpt-4o-mini` - 60% cheaper, good quality
- `gpt-4-turbo` - Faster inference

**Pricing**:
- GPT-4o: $2.50/1M input, $10/1M output tokens
- GPT-4o-mini: $0.15/1M input, $0.60/1M output tokens

### Anthropic Claude

**Best for**: Code analysis, strong reasoning, privacy-conscious

```bash
CHIMERA_DEFAULT_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_BASE_URL=  # Optional
ANTHROPIC_VERSION=2023-06-01
ANTHROPIC_TEMPERATURE=0.7
ANTHROPIC_MAX_TOKENS=2048
```

**Setup Steps**:
1. Get API key: https://console.anthropic.com/settings/keys
2. Set `ANTHROPIC_API_KEY` in `.env`
3. Choose model (recommended: claude-3-5-sonnet-20241022)
4. Start Chimera

**Recommended Models**:
- `claude-3-5-sonnet-20241022` - Best overall
- `claude-3-5-haiku-20241022` - Fast and cost-effective
- `claude-3-opus-20240229` - Maximum capability

**Pricing**:
- Claude 3.5 Sonnet: $3/1M input, $15/1M output tokens
- Claude 3.5 Haiku: $0.80/1M input, $4/1M output tokens

### IBM Watsonx

**Best for**: Enterprise, regulated industries, open models

```bash
CHIMERA_DEFAULT_PROVIDER=watsonx
WATSONX_API_KEY=your-ibm-api-key
WATSONX_PROJECT_ID=your-project-id
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct
WATSONX_BASE_URL=https://us-south.ml.cloud.ibm.com
WATSONX_TEMPERATURE=0.3
WATSONX_MAX_TOKENS=1024
```

**Setup Steps**:
1. Create IBM Cloud account: https://cloud.ibm.com
2. Get API key: https://cloud.ibm.com/iam/apikeys
3. Create Watsonx project: https://dataplatform.cloud.ibm.com/projects
4. Copy Project ID from project settings
5. Set environment variables
6. Start Chimera

**Recommended Models**:
- `ibm/granite-3-8b-instruct` - IBM's code/instruct model
- `meta-llama/llama-3-1-70b-instruct` - Meta Llama 3.1
- `mistralai/mixtral-8x7b-instruct-v01` - Mixtral MoE

**Features**:
- ✅ Enterprise-grade SLAs
- ✅ GDPR/HIPAA compliance options
- ✅ Open source models
- ✅ Free tier available

### Ollama (Local Models)

**Best for**: Development, privacy, no API costs, offline use

```bash
CHIMERA_DEFAULT_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llava:latest
OLLAMA_TEMPERATURE=0.7
OLLAMA_TIMEOUT=120
```

**Setup Steps**:
```bash
# Automated setup
./scripts/setup_ollama.sh

# Or manual setup
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull llava:latest
```

**Recommended Models**:

*Vision Models (multimodal):*
- `llava:latest` - Best local vision model (7B)
- `llava:13b` - Higher quality, slower
- `bakllava` - Optimized vision model

*Code Models:*
- `deepseek-coder:latest` - Best code generation
- `codellama:latest` - Meta's code model
- `starcoder2:latest` - GitHub's code model

*General Models:*
- `llama3.2:latest` - Latest Meta model
- `gemma:2b` - Fast, lightweight
- `phi3:mini` - Microsoft's efficient model

*Fast Models (< 2GB):*
- `gemma:2b` - Google's 2B model
- `qwen2:1.5b` - Alibaba's efficient model
- `phi3:mini` - Excellent quality/size ratio

**Hardware Requirements**:
- 7B models: 8GB RAM minimum
- 13B models: 16GB RAM minimum
- 70B models: 64GB RAM + GPU recommended

## Multi-Monitor Setup

Chimera supports monitoring any screen in multi-monitor setups.

### Configuration

In the UI:
1. Click **Settings** button
2. Go to **General** tab
3. Select screen from **Monitor** dropdown
4. Click **Save**

### Screen Options

- **Primary Monitor** (default)
- **Secondary Monitor**
- **Extended Display 1**
- **Extended Display 2**

The selected screen will show a green border when monitoring is active.

### Programmatic Configuration

```python
# backend/core/settings.py
class AppSettings(BaseSettings):
    selected_monitor: int = Field(default=0, description="Monitor index to capture")
```

## Privacy Settings

### Screenshot Storage

**Default: Disabled** (recommended)

```bash
STORE_SCREENSHOTS=false  # Don't store screenshots on server
```

When enabled:
```bash
STORE_SCREENSHOTS=true
SCREENSHOT_RETENTION_DAYS=7  # Auto-delete after 7 days
SCREENSHOT_PATH=backend/static/screenshots
```

### Analytics

**Default: Disabled**

```bash
ANALYTICS_ENABLED=false  # No usage tracking
```

### Data Handling

By default, Chimera:
- ✅ Processes screenshots in memory only
- ✅ Deletes screenshots immediately after analysis
- ✅ Never sends data to third parties (except chosen LLM provider)
- ✅ Supports fully offline mode with Ollama

### GDPR/Privacy Compliance

For EU/privacy-sensitive deployments:

```bash
# Use local Ollama (no data leaves machine)
CHIMERA_DEFAULT_PROVIDER=ollama

# Or use EU-based providers
ANTHROPIC_BASE_URL=https://api.anthropic.eu  # If available
WATSONX_BASE_URL=https://eu-de.ml.cloud.ibm.com

# Disable all telemetry
STORE_SCREENSHOTS=false
ANALYTICS_ENABLED=false
```

## Production Deployment

### Recommended Settings

```bash
# .env.production
APP_NAME="Chimera Desktop Assistant"
DEBUG=false
LOG_LEVEL=WARNING

# Use production provider
CHIMERA_DEFAULT_PROVIDER=openai
OPENAI_API_KEY=sk-prod-key-here
OPENAI_MODEL=gpt-4o

# Security
HOST=127.0.0.1  # Only local access
PORT=8000
RELOAD=false

# Privacy
STORE_SCREENSHOTS=false
ANALYTICS_ENABLED=false
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync --no-dev

EXPOSE 8000
CMD ["uv", "run", "chimera-serve"]
```

```bash
# Build and run
docker build -t chimera .
docker run -p 8000:8000 --env-file .env.production chimera
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chimera
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: chimera
        image: chimera:latest
        env:
        - name: CHIMERA_DEFAULT_PROVIDER
          value: "openai"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: chimera-secrets
              key: openai-api-key
```

### Systemd Service (Linux)

```ini
# /etc/systemd/system/chimera.service
[Unit]
Description=Chimera Desktop Assistant
After=network.target

[Service]
Type=simple
User=chimera
WorkingDirectory=/opt/chimera
EnvironmentFile=/opt/chimera/.env
ExecStart=/usr/local/bin/uv run chimera-serve
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable chimera
sudo systemctl start chimera
sudo systemctl status chimera
```

## Advanced Configuration

### Custom Model Endpoints

Use custom OpenAI-compatible endpoints:

```bash
# Local LLM server (LM Studio, LocalAI, etc.)
OPENAI_BASE_URL=http://localhost:1234/v1
OPENAI_API_KEY=not-required
OPENAI_MODEL=local-model-name
```

### Rate Limiting

```python
# backend/core/settings.py (add custom settings)
class AppSettings(BaseSettings):
    rate_limit_requests: int = Field(default=100, description="Max requests per minute")
    rate_limit_window: int = Field(default=60, description="Rate limit window (seconds)")
```

### Logging Configuration

```bash
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json  # json or text
LOG_FILE=logs/chimera.log
```

### Multi-User Configuration

For enterprise multi-user setups:

```bash
# Enable user authentication
ENABLE_AUTH=true
AUTH_PROVIDER=oauth  # oauth, ldap, saml
AUTH_SECRET_KEY=your-secret-key

# User-specific quotas
USER_QUOTA_REQUESTS=1000
USER_QUOTA_WINDOW=86400  # 24 hours
```

## Troubleshooting

### Provider Connection Issues

```bash
# Test OpenAI connection
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Test Claude connection
curl https://api.anthropic.com/v1/models \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01"

# Test Ollama connection
curl http://127.0.0.1:11434/api/tags
```

### Configuration Validation

```bash
# Validate configuration
uv run python -c "from backend.core.settings import get_settings; print(get_settings())"

# Check provider is configured
uv run python -c "from backend.core.llm_provider import build_llm; print(build_llm())"
```

### Environment Loading Issues

```bash
# Check if .env is loaded
uv run python -c "import os; print(os.getenv('CHIMERA_DEFAULT_PROVIDER'))"

# Force reload settings
uv run python -c "from backend.core.settings import reload_settings; print(reload_settings())"
```

## Resources

- [Environment Variables Reference](.env.example)
- [Testing Guide](./TESTING.md)
- [API Documentation](./API.md)
- [LLM Provider Documentation](../backend/core/README.md)

---

**Last Updated**: 2025-12-26
**Maintained by**: Chimera Development Team
