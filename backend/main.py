from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import uuid
from typing import Any

from backend.core.manager import engine
from backend.core.tools import tool_schemas, run_tool

app = FastAPI(title="Chimera Enterprise API v2.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="backend/static"), name="static")

@app.on_event("startup")
async def startup():
    engine.load_plugins()
    await engine.start_engine()

# -------- Health Check Endpoint --------
@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for monitoring and CI/CD
    Returns system status and version information
    """
    from backend.core.settings import get_settings
    settings = get_settings()

    return {
        "status": "healthy",
        "version": "2.1.0",
        "app_name": settings.app_name,
        "provider": settings.provider.value,
        "plugins_loaded": len(engine.heads),
    }

# -------- OpenAI-like Chat Endpoint --------
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatReq(BaseModel):
    model: str
    messages: list[ChatMessage]

@app.post("/v1/chat/completions")
async def openai_chat(req: ChatReq):
    try:
        head = req.model.lower()
        if head not in engine.heads:
            head = "ollama" if "ollama" in engine.heads else list(engine.heads.keys())[0]
        prompt = req.messages[-1].content
        resp = await engine.process(head, prompt)
        return {"id": "chimera-gen", "choices": [{"message": {"role": "assistant", "content": resp}}]}
    except Exception as e:
        raise HTTPException(500, str(e))

# -------- Vision Endpoint (browser-head dependent) --------
@app.post("/api/vision")
async def vision_chat(
    model: str = Form(...),
    prompt: str = Form(...),
    file: UploadFile = File(...)
):
    temp_path = f"backend/static/{uuid.uuid4()}_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        resp = await engine.process(model, prompt, image_path=os.path.abspath(temp_path))
        return {"response": resp}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# -------- Admin Status --------
@app.get("/api/status")
async def get_status():
    return {
        "plugins": list(engine.heads.keys()),
        "active_sessions": await engine.capture_state(),
        "tools": tool_schemas(),
    }

@app.post("/api/spawn/{model}")
async def spawn_head(model: str):
    await engine.get_page(model)
    return {"status": "Spawned"}

# -------- Computer Use (Playwright Tools) --------
class ToolReq(BaseModel):
    tool: str
    args: dict[str, Any] = {}

@app.post("/api/computer/{model}/tool")
async def computer_tool(model: str, req: ToolReq):
    """
    Execute a single computer-use tool against a browser model session.
    Example tools: goto, click, type, scroll, wait
    """
    if model not in engine.heads:
        raise HTTPException(404, "Unknown model")
    
    head = engine.heads[model]
    if not head.supports_browser:
        raise HTTPException(400, f"Model '{model}' does not support browser sessions.")
        
    page = await engine.get_page(model)
    try:
        result = await run_tool(page, req.tool, req.args or {})
        return {"model": model, "result": result}
    except Exception as e:
        raise HTTPException(500, str(e))

def start():
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
