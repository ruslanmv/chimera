"""
Chimera Enterprise - Google Gemini Plugin
Supports Gemini Pro, Gemini Pro Vision, and other Google AI models
"""

import os
import logging
from typing import Any, Dict, Optional, List

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("google-generativeai not installed. Install with: uv add google-generativeai")

from backend.core.plugin_base import BaseLLMHead


class GeminiHead(BaseLLMHead):
    """
    Google Gemini LLM provider

    Supports:
    - Gemini 2.0 Flash (gemini-2.0-flash-exp)
    - Gemini 1.5 Pro (gemini-1.5-pro)
    - Gemini 1.5 Flash (gemini-1.5-flash)
    - Vision capabilities
    - Function calling
    """

    # Class variable for plugin discovery
    plugin_name = "gemini"

    @property
    def name(self) -> str:
        """Plugin name for discovery"""
        return "gemini"

    def __init__(self):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai library not installed")

        # Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY or GEMINI_API_KEY environment variable required.\n"
                "Get your key at: https://makersuite.google.com/app/apikey"
            )

        genai.configure(api_key=api_key)
        self.default_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        self.logger = logging.getLogger(__name__)

        self.logger.info(f"✓ Gemini plugin initialized (model: {self.default_model})")

    async def generate_text(self, page: Any, prompt: str) -> str:
        """
        Generate text response (required by BaseLLMHead)

        Args:
            page: Not used for API-based provider (None)
            prompt: User prompt

        Returns:
            Generated text response
        """
        try:
            model = genai.GenerativeModel(self.default_model)
            response = await model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Gemini generate_text error: {e}")
            return f"Error: {str(e)}"

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

        # Initialize model
        model = genai.GenerativeModel(model_name)

        # Convert OpenAI messages to Gemini format
        gemini_messages = self._convert_messages(messages)

        try:
            # Generate response
            response = await model.generate_content_async(
                gemini_messages,
                generation_config={
                    "temperature": request.get("temperature", 0.7),
                    "max_output_tokens": request.get("max_tokens", 8192),
                }
            )

            # Convert to OpenAI format
            return {
                "id": f"gemini-{model_name}",
                "object": "chat.completion",
                "model": model_name,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response.text
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0,
                    "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
                }
            }

        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            raise

    def _convert_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Convert OpenAI message format to Gemini format"""
        gemini_messages = []

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            # Map roles
            if role == "system":
                # Gemini doesn't have system messages, prepend to first user message
                gemini_messages.append({
                    "role": "user",
                    "parts": [f"System instruction: {content}"]
                })
            elif role == "user":
                gemini_messages.append({
                    "role": "user",
                    "parts": [content]
                })
            elif role == "assistant":
                gemini_messages.append({
                    "role": "model",
                    "parts": [content]
                })

        return gemini_messages

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
            model: Model name (defaults to gemini-pro-vision)

        Returns:
            Model response text
        """
        model_name = model or "gemini-1.5-flash"
        gemini_model = genai.GenerativeModel(model_name)

        # Upload image
        from PIL import Image
        import io
        image = Image.open(io.BytesIO(image_data))

        # Generate response
        response = await gemini_model.generate_content_async([prompt, image])
        return response.text

    def supports_vision(self) -> bool:
        """Check if provider supports vision"""
        return True

    def get_available_models(self) -> List[str]:
        """List available Gemini models"""
        return [
            "gemini-2.0-flash-exp",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro"
        ]
