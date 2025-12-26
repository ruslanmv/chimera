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
        except Exception as e:
            return f"[ollama error] {e}"
