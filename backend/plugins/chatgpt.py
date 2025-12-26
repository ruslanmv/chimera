from playwright.async_api import Page
from backend.core.plugin_base import BaseLLMHead

class ChatGPTHead(BaseLLMHead):
    @property
    def name(self): return "chatgpt"

    @property
    def start_url(self): return "https://chatgpt.com"

    @property
    def supports_vision(self) -> bool:
        return True

    async def generate_text(self, page: Page, prompt: str) -> str:
        TEXT_AREA = "#prompt-textarea"
        SEND_BTN = "button[data-testid='send-button']"
        
        await page.wait_for_selector(TEXT_AREA)
        await page.fill(TEXT_AREA, prompt)
        await page.click(SEND_BTN)
        
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2500)
        
        divs = await page.locator("div.markdown").all_text_contents()
        return divs[-1] if divs else "No response."

    async def generate_with_image(self, page: Page, prompt: str, image_path: str) -> str:
        FILE_INPUT = "input[type='file']"
        await page.set_input_files(FILE_INPUT, image_path)
        await page.wait_for_timeout(1500) 
        return await self.generate_text(page, prompt)
