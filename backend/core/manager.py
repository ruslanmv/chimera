import importlib
import os
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

from .config import DATA_DIR, settings, SCREENSHOT_DIR
from .plugin_base import BaseLLMHead

class ChimeraManager:
    def __init__(self):
        self.playwright = None
        self.context = None
        self.heads: dict[str, BaseLLMHead] = {}
        self.active_pages = {}
        self.locks = {}

    def load_plugins(self):
        plugin_dir = Path("backend/plugins")
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"backend.plugins.{filename[:-3]}"
                module = importlib.import_module(module_name)
                
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, BaseLLMHead) and attr is not BaseLLMHead:
                        instance = attr()
                        self.heads[instance.name] = instance
                        self.locks[instance.name] = asyncio.Lock()
                        print(f"🧩 Plugin Loaded: {instance.name}")

    async def start_engine(self):
        self.playwright = await async_playwright().start()
        
        # We only need a persistent browser context for "browser heads".
        # But starting it always is fine and keeps architecture simple.
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=DATA_DIR,
            headless=settings.CHIMERA_HEADLESS,
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1280, "height": 800}
        )

    async def get_page(self, head_name: str):
        if head_name not in self.heads:
            raise ValueError("Unknown head")
        
        head = self.heads[head_name]
        if not head.supports_browser:
            raise ValueError(f"Head '{head_name}' does not use a browser page.")

        if head_name in self.active_pages and not self.active_pages[head_name].is_closed():
            return self.active_pages[head_name]
            
        print(f"🔌 Spawning {head_name} browser session...")
        page = await self.context.new_page()
        await stealth_async(page)
        await page.goto(head.start_url)
        self.active_pages[head_name] = page
        return page

    async def process(self, head_name: str, prompt: str, image_path: str = None):
        if head_name not in self.heads:
            raise ValueError("Unknown head")

        async with self.locks[head_name]:
            head = self.heads[head_name]
            page = None
            
            if head.supports_browser:
                page = await self.get_page(head_name)
                await page.bring_to_front()
            
            if image_path:
                return await head.generate_with_image(page, prompt, image_path)
            return await head.generate_text(page, prompt)

    async def capture_state(self):
        status = []
        for name, page in self.active_pages.items():
            if not page.is_closed():
                path = SCREENSHOT_DIR / f"{name}.png"
                try:
                    await page.screenshot(path=path, type="png")
                    status.append({"name": name, "status": "active", "screenshot": f"/static/screenshots/{name}.png"})
                except Exception as e:
                    status.append({"name": name, "status": "error", "error": str(e)})
        return status

engine = ChimeraManager()
