from abc import ABC, abstractmethod
from playwright.async_api import Page

class BaseLLMHead(ABC):
    """Base class contract for all LLM 'heads'."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def start_url(self) -> str:
        """Only relevant for browser-driven providers (ChatGPT web, etc)."""
        return ""

    @property
    def supports_browser(self) -> bool:
        return bool(self.start_url)

    @property
    def supports_vision(self) -> bool:
        return False

    @property
    def supports_tools(self) -> bool:
        """If true, the head can accept tool results / structured tool calls (future)."""
        return False

    @abstractmethod
    async def generate_text(self, page: Page | None, prompt: str) -> str:
        pass

    async def generate_with_image(self, page: Page, prompt: str, image_path: str) -> str:
        raise NotImplementedError("This head does not support Vision yet.")
