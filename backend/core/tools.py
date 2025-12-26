"""
Tool registry.

Today:
- exposes 'computer use' tools for browser heads
- exposes minimal local tools (read/write can be added safely later)

Tomorrow:
- you can bridge MCP servers here and auto-register tools.
"""

from __future__ import annotations

from typing import Any, Callable, Awaitable
from playwright.async_api import Page

from .computer_use import tool_goto, tool_click, tool_type, tool_scroll, tool_wait
from .config import settings

ToolFn = Callable[..., Awaitable[dict[str, Any]]]

async def _wrap(fn, *args, **kwargs):
    res = await fn(*args, **kwargs)
    return {"ok": res.ok, "message": res.message, "data": res.data}

def tool_schemas() -> list[dict[str, Any]]:
    """Light schema list for UI + future tool-aware models."""
    return [
        {"name": "goto", "args": {"url": "string"}, "desc": "Navigate browser to URL (optionally domain-restricted)."},
        {"name": "click", "args": {"selector": "string"}, "desc": "Click an element via CSS selector."},
        {"name": "type", "args": {"selector": "string", "text": "string", "clear": "bool"}, "desc": "Type into an input/textarea."},
        {"name": "scroll", "args": {"dy": "int"}, "desc": "Scroll page by dy pixels."},
        {"name": "wait", "args": {"ms": "int"}, "desc": "Wait for ms milliseconds."},
    ]

async def run_tool(page: Page, name: str, args: dict[str, Any]) -> dict[str, Any]:
    name = name.lower().strip()
    
    if name == "goto":
        return await _wrap(tool_goto, page, args["url"], settings.CHIMERA_ALLOWED_DOMAINS)
    if name == "click":
        return await _wrap(tool_click, page, args["selector"])
    if name == "type":
        return await _wrap(tool_type, page, args["selector"], args.get("text", ""), bool(args.get("clear", True)))
    if name == "scroll":
        return await _wrap(tool_scroll, page, int(args.get("dy", 800)))
    if name == "wait":
        return await _wrap(tool_wait, page, int(args.get("ms", 1000)))

    return {"ok": False, "message": f"Unknown tool: {name}", "data": None}
