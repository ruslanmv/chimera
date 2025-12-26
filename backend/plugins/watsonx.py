"""
Chimera Enterprise - IBM watsonx.ai Plugin
Supports IBM's enterprise LLM models including Granite, Llama, and Mixtral
"""

import os
import logging
from typing import Any, Dict, Optional, List

try:
    from ibm_watsonx_ai import APIClient, Credentials
    from ibm_watsonx_ai.foundation_models import Model
    WATSONX_AVAILABLE = True
except ImportError:
    WATSONX_AVAILABLE = False
    logging.warning("ibm-watsonx-ai not installed. Install with: uv add ibm-watsonx-ai")

from backend.core.plugin_base import BaseLLMHead


class WatsonXHead(BaseLLMHead):
    """
    IBM watsonx.ai LLM provider

    Supports:
    - IBM Granite models
    - Meta Llama models
    - Mistral Mixtral models
    - Enterprise features (governance, cost tracking, etc.)
    """

    # Class variable for plugin discovery
    plugin_name = "watsonx"

    def __init__(self):
        if not WATSONX_AVAILABLE:
            raise ImportError("ibm-watsonx-ai library not installed")

        # Get credentials from environment
        api_key = os.getenv("WATSONX_API_KEY") or os.getenv("IBM_API_KEY")
        project_id = os.getenv("WATSONX_PROJECT_ID")
        url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")

        if not api_key or not project_id:
            raise ValueError(
                "WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables required.\n"
                "Get credentials at: https://cloud.ibm.com/watsonx"
            )

        # Initialize Watson client
        credentials = Credentials(
            url=url,
            api_key=api_key
        )

        self.client = APIClient(credentials)
        self.project_id = project_id
        self.default_model = os.getenv("WATSONX_MODEL", "ibm/granite-13b-chat-v2")
        self.logger = logging.getLogger(__name__)

        self.logger.info(f"✓ WatsonX plugin initialized (model: {self.default_model})")

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

        # Convert messages to prompt
        prompt = self._messages_to_prompt(messages)

        # Model parameters
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": request.get("max_tokens", 2048),
            "temperature": request.get("temperature", 0.7),
            "top_k": 50,
            "top_p": 1
        }

        try:
            # Initialize model
            model = Model(
                model_id=model_name,
                params=parameters,
                credentials=self.client.credentials,
                project_id=self.project_id
            )

            # Generate response
            response = model.generate_text(prompt)

            # Convert to OpenAI format
            return {
                "id": f"watsonx-{model_name}",
                "object": "chat.completion",
                "model": model_name,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": len(prompt.split()),  # Approximate
                    "completion_tokens": len(response.split()),
                    "total_tokens": len(prompt.split()) + len(response.split())
                }
            }

        except Exception as e:
            self.logger.error(f"WatsonX API error: {e}")
            raise

    def _messages_to_prompt(self, messages: List[Dict[str, Any]]) -> str:
        """Convert OpenAI messages to a single prompt string"""
        prompt_parts = []

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                prompt_parts.append(f"System: {content}\n")
            elif role == "user":
                prompt_parts.append(f"User: {content}\n")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}\n")

        prompt_parts.append("Assistant:")
        return "\n".join(prompt_parts)

    async def vision_completion(
        self,
        prompt: str,
        image_data: bytes,
        model: Optional[str] = None
    ) -> str:
        """
        Handle vision requests (not yet supported by WatsonX)

        Args:
            prompt: Text prompt
            image_data: Image bytes
            model: Model name

        Returns:
            Error message
        """
        raise NotImplementedError(
            "Vision capabilities not yet available in watsonx.ai. "
            "Check IBM documentation for multimodal model updates."
        )

    def supports_vision(self) -> bool:
        """Check if provider supports vision"""
        return False

    def get_available_models(self) -> List[str]:
        """List available WatsonX models"""
        return [
            "ibm/granite-13b-chat-v2",
            "ibm/granite-13b-instruct-v2",
            "meta-llama/llama-3-70b-instruct",
            "meta-llama/llama-3-8b-instruct",
            "mistralai/mixtral-8x7b-instruct-v01",
            "google/flan-ul2",
            "bigscience/mt0-xxl"
        ]
