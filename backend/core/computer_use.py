from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from playwright.async_api import Page

@dataclass
class ToolResult:
    ok: bool
    message: str
    data: dict | None = None

def _domain_allowed(url: str, allowed_domains_csv: str) -> bool:
    if not allowed_domains_csv.strip():
        return True
    allowed = {d.strip().lower() for d in allowed_domains_csv.split(",") if d.strip()}
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in allowed)

async def tool_goto(page: Page, url: str, allowed_domains_csv: str) -> ToolResult:
    if not _domain_allowed(url, allowed_domains_csv):
        return ToolResult(False, f"Blocked by domain allowlist: {url}")
    await page.goto(url)
    return ToolResult(True, "Navigated", {"url": url})

async def tool_click(page: Page, selector: str) -> ToolResult:
    await page.wait_for_selector(selector, timeout=20000)
    await page.click(selector)
    return ToolResult(True, "Clicked", {"selector": selector})

async def tool_type(page: Page, selector: str, text: str, clear: bool = True) -> ToolResult:
    await page.wait_for_selector(selector, timeout=20000)
    if clear:
        await page.fill(selector, "")
    await page.type(selector, text, delay=10)
    return ToolResult(True, "Typed", {"selector": selector, "chars": len(text)})

async def tool_scroll(page: Page, dy: int = 800) -> ToolResult:
    await page.mouse.wheel(0, dy)
    return ToolResult(True, "Scrolled", {"dy": dy})

async def tool_wait(page: Page, ms: int = 1000) -> ToolResult:
    await page.wait_for_timeout(ms)
    return ToolResult(True, "Waited", {"ms": ms})
