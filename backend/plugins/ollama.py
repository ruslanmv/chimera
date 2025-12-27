import httpx
from backend.core.plugin_base import BaseLLMHead
from backend.core.config import settings

class OllamaHead(BaseLLMHead):
    """
    Local LLM head using Ollama. 
    - No browser required
    - Great default for OSS / privacy crowd
    """

    @property
    def name(self): return "ollama"

    async def generate_text(self, page, prompt: str) -> str:
        url = f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/generate"
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                r = await client.post(url, json=payload)
                r.raise_for_status()
                data = r.json()
                return data.get("response", "").strip() or "No response."
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return f"[ollama error] Ollama server is running but model '{settings.OLLAMA_MODEL}' not found. Please run: ollama pull {settings.OLLAMA_MODEL}"
            return f"[ollama error] HTTP {e.response.status_code}: {e.response.text}"
        except httpx.ConnectError:
            return f"[ollama error] Cannot connect to Ollama server at {settings.OLLAMA_BASE_URL}. Please ensure Ollama is running with: ollama serve"
        except httpx.TimeoutException:
            return f"[ollama error] Request timeout. The model might be loading or processing is slow."
        except Exception as e:
            return f"[ollama error] {type(e).__name__}: {e}"
