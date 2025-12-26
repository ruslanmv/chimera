"""
Chimera Enterprise - Anthropic Claude Plugin
Supports Claude 3.7 Sonnet, Claude Opus, and other Anthropic models
"""

import os
import logging
from typing import Any, Dict, Optional, List
import base64

try:
    from anthropic import AsyncAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logging.warning("anthropic not installed. Install with: uv add anthropic")

from backend.core.plugin_base import BaseLLMHead


class ClaudeHead(BaseLLMHead):
    """
    Anthropic Claude LLM provider

    Supports:
    - Claude 3.7 Sonnet (claude-3-7-sonnet-20250219)
    - Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)
    - Claude 3 Opus (claude-3-opus-20240229)
    - Claude 3 Haiku (claude-3-haiku-20240307)
    - Vision capabilities
    - Tool use / Function calling
    """

    # Class variable for plugin discovery
    plugin_name = "claude"

    def __init__(self):
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic library not installed")

        # Get API key from environment
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable required.\n"
                "Get your key at: https://console.anthropic.com/"
            )

        self.client = AsyncAnthropic(api_key=api_key)
        self.default_model = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
        self.logger = logging.getLogger(__name__)

        self.logger.info(f"✓ Claude plugin initialized (model: {self.default_model})")

    async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle chat completion request

        Args:
            request: OpenAI-compatible request with 'model' and 'messages'

        Returns:
            OpenAI-compatible response
        """
        model_name = request.get("model", self.default_model)
        messages = request.get("messages", [])

        # Extract system message
        system_message = None
        claude_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                claude_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        try:
            # Call Claude API
            response = await self.client.messages.create(
                model=model_name,
                max_tokens=request.get("max_tokens", 8192),
                temperature=request.get("temperature", 0.7),
                system=system_message,
                messages=claude_messages
            )

            # Convert to OpenAI format
            return {
                "id": response.id,
                "object": "chat.completion",
                "model": model_name,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response.content[0].text
                    },
                    "finish_reason": response.stop_reason
                }],
                "usage": {
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            }

        except Exception as e:
            self.logger.error(f"Claude API error: {e}")
            raise

    async def vision_completion(
        self,
        prompt: str,
        image_data: bytes,
        model: Optional[str] = None
    ) -> str:
        """
        Handle vision requests

        Args:
            prompt: Text prompt
            image_data: Image bytes
            model: Model name

        Returns:
            Model response text
        """
        model_name = model or self.default_model

        # Encode image to base64
        image_b64 = base64.b64encode(image_data).decode('utf-8')

        # Detect media type (simplified - assumes PNG/JPEG)
        media_type = "image/png"
        if image_data.startswith(b'\xff\xd8'):
            media_type = "image/jpeg"

        # Create message with image
        response = await self.client.messages.create(
            model=model_name,
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_b64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }]
        )

        return response.content[0].text

    def supports_vision(self) -> bool:
        """Check if provider supports vision"""
        return True

    def get_available_models(self) -> List[str]:
        """List available Claude models"""
        return [
            "claude-3-7-sonnet-20250219",
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229",
            "claude-3-haiku-20240307"
        ]
