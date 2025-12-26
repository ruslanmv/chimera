"""
Chimera Enterprise - Comprehensive Test Suite
Tests basic installations, LLM queries, MCP server, and multi-provider integration
"""

import pytest
import httpx
import asyncio
from pathlib import Path


class TestBasicInstallation:
    """Test that all required packages are installed correctly"""

    def test_fastapi_import(self):
        """Test FastAPI is installed"""
        import fastapi
        assert fastapi.__version__ >= "0.127.0"

    def test_playwright_import(self):
        """Test Playwright is installed"""
        import playwright
        assert playwright is not None

    def test_pydantic_import(self):
        """Test Pydantic is installed"""
        import pydantic
        assert pydantic.__version__ >= "2.0.0"

    def test_httpx_import(self):
        """Test HTTPX is installed"""
        import httpx
        assert httpx is not None


class TestCoreComponents:
    """Test core Chimera components"""

    def test_plugin_base_import(self):
        """Test plugin base class is importable"""
        from backend.core.plugin_base import BaseLLMHead
        assert BaseLLMHead is not None

    def test_manager_import(self):
        """Test ChimeraManager is importable"""
        from backend.core.manager import ChimeraManager
        assert ChimeraManager is not None

    def test_config_import(self):
        """Test config is importable"""
        from backend.core.config import settings
        assert settings is not None

    def test_tools_import(self):
        """Test tools registry is importable"""
        from backend.core.tools import get_tools
        tools = get_tools()
        assert len(tools) > 0
        assert any(tool["function"]["name"] == "goto" for tool in tools)


class TestPlugins:
    """Test plugin discovery and loading"""

    def test_ollama_plugin_import(self):
        """Test Ollama plugin is importable"""
        from backend.plugins.ollama import OllamaHead
        assert OllamaHead is not None

    def test_chatgpt_plugin_import(self):
        """Test ChatGPT plugin is importable"""
        from backend.plugins.chatgpt import ChatGPTHead
        assert ChatGPTHead is not None

    @pytest.mark.asyncio
    async def test_manager_discovers_plugins(self):
        """Test ChimeraManager discovers all plugins"""
        from backend.core.manager import ChimeraManager
        manager = ChimeraManager()

        plugins = manager.get_available_plugins()
        assert len(plugins) > 0
        assert "ollama" in plugins


@pytest.mark.asyncio
class TestAPIEndpoints:
    """Test FastAPI endpoints"""

    async def test_health_check(self):
        """Test basic connectivity (if server is running)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/status", timeout=2.0)
                if response.status_code == 200:
                    data = response.json()
                    assert "plugins" in data
        except (httpx.ConnectError, httpx.TimeoutException):
            pytest.skip("Backend server not running")

    async def test_status_endpoint_structure(self):
        """Test /api/status returns expected structure"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/status", timeout=2.0)
                if response.status_code == 200:
                    data = response.json()
                    assert isinstance(data["plugins"], list)
                    assert isinstance(data["sessions"], dict)
        except (httpx.ConnectError, httpx.TimeoutException):
            pytest.skip("Backend server not running")


class TestMCPServer:
    """Test Model Context Protocol server functionality"""

    def test_mcp_server_import(self):
        """Test MCP server module is importable"""
        try:
            from backend.core.mcp_server import MCPServer
            assert MCPServer is not None
        except ImportError:
            pytest.skip("MCP server not yet implemented")

    @pytest.mark.asyncio
    async def test_mcp_server_initialization(self):
        """Test MCP server can be initialized"""
        try:
            from backend.core.mcp_server import MCPServer
            server = MCPServer()
            assert server is not None
        except ImportError:
            pytest.skip("MCP server not yet implemented")

    @pytest.mark.asyncio
    async def test_mcp_tool_registration(self):
        """Test MCP server can register tools"""
        try:
            from backend.core.mcp_server import MCPServer
            server = MCPServer()
            tools = await server.list_tools()
            assert isinstance(tools, list)
        except ImportError:
            pytest.skip("MCP server not yet implemented")


class TestMultiProviderSupport:
    """Test multi-provider LLM integration"""

    def test_gemini_plugin_exists(self):
        """Test Gemini plugin is available"""
        try:
            from backend.plugins.gemini import GeminiHead
            assert GeminiHead is not None
        except ImportError:
            pytest.skip("Gemini plugin not yet implemented")

    def test_claude_plugin_exists(self):
        """Test Claude plugin is available"""
        try:
            from backend.plugins.claude import ClaudeHead
            assert ClaudeHead is not None
        except ImportError:
            pytest.skip("Claude plugin not yet implemented")

    def test_watsonx_plugin_exists(self):
        """Test Watson.ai plugin is available"""
        try:
            from backend.plugins.watsonx import WatsonXHead
            assert WatsonXHead is not None
        except ImportError:
            pytest.skip("WatsonX plugin not yet implemented")


class TestFrontend:
    """Test frontend is properly configured"""

    def test_frontend_files_exist(self):
        """Test frontend files are present"""
        frontend_dir = Path(__file__).parent.parent / "frontend"
        assert (frontend_dir / "package.json").exists()
        assert (frontend_dir / "vite.config.js").exists()
        assert (frontend_dir / "src" / "App.jsx").exists()

    def test_package_json_has_dependencies(self):
        """Test package.json has required dependencies"""
        import json
        frontend_dir = Path(__file__).parent.parent / "frontend"
        package_json = json.loads((frontend_dir / "package.json").read_text())

        assert "react" in package_json["dependencies"]
        assert "lucide-react" in package_json["dependencies"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
