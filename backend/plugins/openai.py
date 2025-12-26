"""
Chimera Enterprise - OpenAI API Plugin
Direct API integration for ChatGPT, GPT-4, and other OpenAI models
"""

import os
import logging
from typing import Any, Dict, Optional, List
import base64

try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("openai not installed. Install with: uv add openai")

from backend.core.plugin_base import BaseLLMHead


class OpenAIHead(BaseLLMHead):
    """
    OpenAI API LLM provider

    Supports:
    - GPT-4 Turbo (gpt-4-turbo)
    - GPT-4 (gpt-4)
    - GPT-3.5 Turbo (gpt-3.5-turbo)
    - Vision capabilities (GPT-4V)
    - Function calling
    """

    # Class variable for plugin discovery
    plugin_name = "openai"

    def __init__(self):
        if not OPENAI_AVAILABLE:
            raise ImportError("openai library not installed")

        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable required.\n"
                "Get your key at: https://platform.openai.com/api-keys"
            )

        self.client = AsyncOpenAI(api_key=api_key)
        self.default_model = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
        self.logger = logging.getLogger(__name__)

        self.logger.info(f"✓ OpenAI plugin initialized (model: {self.default_model})")

    async def chat_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle chat completion request

        Args:
            request: OpenAI-compatible request with 'model' and 'messages'

        Returns:
            OpenAI-compatible response
        """
        try:
            # Direct passthrough to OpenAI API
            response = await self.client.chat.completions.create(
                model=request.get("model", self.default_model),
                messages=request.get("messages", []),
                temperature=request.get("temperature", 0.7),
                max_tokens=request.get("max_tokens"),
                stream=False
            )

            # Convert to dict format
            return {
                "id": response.id,
                "object": response.object,
                "model": response.model,
                "choices": [{
                    "index": choice.index,
                    "message": {
                        "role": choice.message.role,
                        "content": choice.message.content
                    },
                    "finish_reason": choice.finish_reason
                } for choice in response.choices],
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }

        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
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
            model: Model name (defaults to gpt-4-vision-preview)

        Returns:
            Model response text
        """
        model_name = model or "gpt-4-vision-preview"

        # Encode image to base64
        image_b64 = base64.b64encode(image_data).decode('utf-8')

        # Detect media type
        media_type = "image/png"
        if image_data.startswith(b'\xff\xd8'):
            media_type = "image/jpeg"

        # Create message with image
        response = await self.client.chat.completions.create(
            model=model_name,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{image_b64}"
                        }
                    }
                ]
            }],
            max_tokens=4096
        )

        return response.choices[0].message.content

    def supports_vision(self) -> bool:
        """Check if provider supports vision"""
        return True

    def get_available_models(self) -> List[str]:
        """List available OpenAI models"""
        return [
            "gpt-4-turbo",
            "gpt-4",
            "gpt-4-vision-preview",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        ]
