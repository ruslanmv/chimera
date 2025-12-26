"""
Chimera Enterprise - Model Context Protocol (MCP) Server
Bridges Chimera's multi-provider LLM system with MCP clients
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import logging

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp import types
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    logging.warning("MCP library not installed. Install with: uv add mcp")

from backend.core.tools import get_tools, dispatch_tool
from backend.core.manager import ChimeraManager


@dataclass
class MCPServerConfig:
    """Configuration for MCP server"""
    name: str = "chimera-enterprise"
    version: str = "2.1.0"
    description: str = "Multi-provider LLM gateway with browser automation"


class MCPServer:
    """
    Model Context Protocol server for Chimera Enterprise

    Exposes Chimera's capabilities (LLM routing, browser automation, tools)
    to MCP-compatible clients like Claude Desktop, VS Code, etc.
    """

    def __init__(self, config: Optional[MCPServerConfig] = None):
        self.config = config or MCPServerConfig()
        self.manager = ChimeraManager()
        self.logger = logging.getLogger(__name__)

        if not MCP_AVAILABLE:
            raise ImportError(
                "MCP library not available. Install with: uv add mcp"
            )

        # Initialize MCP server
        self.server = Server(self.config.name)
        self._register_handlers()

    def _register_handlers(self):
        """Register MCP protocol handlers"""

        # List available tools
        @self.server.list_tools()
        async def list_tools() -> List[types.Tool]:
            """Return all available Chimera tools as MCP tools"""
            chimera_tools = get_tools()

            mcp_tools = []
            for tool in chimera_tools:
                func = tool["function"]
                mcp_tools.append(
                    types.Tool(
                        name=func["name"],
                        description=func.get("description", ""),
                        inputSchema=func.get("parameters", {})
                    )
                )

            # Add LLM routing tools
            mcp_tools.extend([
                types.Tool(
                    name="query_llm",
                    description="Query any available LLM provider (Ollama, ChatGPT, Claude, Gemini, WatsonX)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "provider": {
                                "type": "string",
                                "description": "LLM provider (ollama, chatgpt, claude, gemini, watsonx)",
                                "enum": ["ollama", "chatgpt", "claude", "gemini", "watsonx"]
                            },
                            "messages": {
                                "type": "array",
                                "description": "Chat messages",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "role": {"type": "string"},
                                        "content": {"type": "string"}
                                    }
                                }
                            },
                            "model": {
                                "type": "string",
                                "description": "Specific model to use (optional)"
                            }
                        },
                        "required": ["provider", "messages"]
                    }
                ),
                types.Tool(
                    name="list_providers",
                    description="List all available LLM providers and their status",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ])

            return mcp_tools

        # Execute tool calls
        @self.server.call_tool()
        async def call_tool(
            name: str,
            arguments: Dict[str, Any]
        ) -> List[types.TextContent]:
            """Execute a Chimera tool and return results"""

            try:
                # Handle LLM routing tools
                if name == "query_llm":
                    result = await self._query_llm(arguments)
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

                elif name == "list_providers":
                    providers = self.manager.get_available_plugins()
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({"providers": providers}, indent=2)
                    )]

                # Handle browser automation tools
                else:
                    result = await dispatch_tool(name, arguments)
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )]

            except Exception as e:
                self.logger.error(f"Tool execution failed: {e}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": str(e),
                        "tool": name,
                        "arguments": arguments
                    }, indent=2)
                )]

        # List available resources (screenshots, logs, etc.)
        @self.server.list_resources()
        async def list_resources() -> List[types.Resource]:
            """List available resources"""
            return [
                types.Resource(
                    uri="chimera://status",
                    name="Chimera Status",
                    mimeType="application/json",
                    description="Current status of all LLM providers and browser sessions"
                ),
                types.Resource(
                    uri="chimera://providers",
                    name="LLM Providers",
                    mimeType="application/json",
                    description="List of available LLM providers"
                )
            ]

        # Read resources
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read a Chimera resource"""
            if uri == "chimera://status":
                plugins = self.manager.get_available_plugins()
                sessions = {}
                for plugin_name in plugins:
                    plugin = self.manager.get_plugin(plugin_name)
                    if hasattr(plugin, 'browser_manager'):
                        sessions[plugin_name] = {
                            "active": plugin.browser_manager is not None
                        }

                return json.dumps({
                    "plugins": plugins,
                    "sessions": sessions
                }, indent=2)

            elif uri == "chimera://providers":
                providers = self.manager.get_available_plugins()
                return json.dumps({
                    "providers": providers,
                    "count": len(providers)
                }, indent=2)

            else:
                raise ValueError(f"Unknown resource: {uri}")

    async def _query_llm(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route LLM query to appropriate provider"""
        provider = arguments["provider"]
        messages = arguments["messages"]
        model = arguments.get("model")

        plugin = self.manager.get_plugin(provider)
        if not plugin:
            raise ValueError(f"Provider not available: {provider}")

        # Create OpenAI-compatible request
        request = {
            "model": model or getattr(plugin, "default_model", "default"),
            "messages": messages
        }

        # Call provider
        response = await plugin.chat_completion(request)
        return response

    async def run(self):
        """Run the MCP server over stdio"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point for MCP server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if not MCP_AVAILABLE:
        print("ERROR: MCP library not installed")
        print("Install with: uv add mcp")
        return

    server = MCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
