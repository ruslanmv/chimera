"""
Chimera Model Catalog
Dynamic model discovery for all supported LLM providers
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

import requests

from .settings import AppSettings, LLMProvider, get_settings


class ModelCatalogError(Exception):
    """Base exception for model catalog errors"""

    pass


# --- Watsonx.ai configuration ---

WATSONX_BASE_URLS = [
    "https://us-south.ml.cloud.ibm.com",
    "https://eu-de.ml.cloud.ibm.com",
    "https://jp-tok.ml.cloud.ibm.com",
    "https://au-syd.ml.cloud.ibm.com",
]

WATSONX_ENDPOINT = "/ml/v1/foundation_model_specs"
WATSONX_PARAMS = {
    "version": "2024-09-16",
    "filters": "!function_embedding,!lifecycle_withdrawn",
}
TODAY = datetime.today().strftime("%Y-%m-%d")


def _is_deprecated_or_withdrawn(lifecycle: List[Dict[str, Any]]) -> bool:
    """Return True if a model lifecycle includes a deprecated/withdrawn item active today."""
    for entry in lifecycle:
        if entry.get("id") in {"deprecated", "withdrawn"} and entry.get(
            "start_date", ""
        ) <= TODAY:
            return True
    return False


# --- Provider-specific listing functions ---


def _list_chimera_server_models(settings: AppSettings) -> Tuple[List[str], Optional[str]]:
    """List models available on Chimera managed server"""
    api_url = settings.chimera_server.api_url
    api_key = settings.chimera_server.api_key or os.getenv("CHIMERA_SERVER_API_KEY")

    url = f"{api_url.rstrip('/')}/models"

    try:
        headers = {}
        if api_key and api_key != "not-required":
            headers["Authorization"] = f"Bearer {api_key}"

        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()

        data = resp.json().get("models", [])
        models = sorted({m.get("id", "") for m in data if m.get("id")})
        return models, None
    except Exception as e:
        # Default models if server is unavailable
        return ["chimera-vision-1", "chimera-code-1", "chimera-general-1"], None


def _list_openai_models(settings: AppSettings) -> Tuple[List[str], Optional[str]]:
    """
    Use OpenAI /v1/models endpoint to list models available to the configured key.
    """
    api_key = settings.openai.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return [], "OpenAI API key not configured"

    base_url = settings.openai.base_url or os.getenv(
        "OPENAI_BASE_URL", "https://api.openai.com"
    )
    url = f"{base_url.rstrip('/')}/v1/models"

    try:
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json().get("data", [])

        # Filter for vision-capable models
        models = []
        for m in data:
            model_id = m.get("id", "")
            if model_id and any(
                x in model_id.lower()
                for x in ["gpt-4", "gpt-4o", "vision"]
            ):
                models.append(model_id)

        return sorted(set(models)), None
    except Exception as e:
        return [], f"Error listing OpenAI models: {e}"


def _list_claude_models(settings: AppSettings) -> Tuple[List[str], Optional[str]]:
    """
    Use Anthropic /v1/models endpoint to list Claude models available to the key.
    """
    api_key = settings.claude.api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return [], "Claude (Anthropic) API key not configured"

    base_url = settings.claude.base_url or os.getenv(
        "ANTHROPIC_BASE_URL", "https://api.anthropic.com"
    )
    url = f"{base_url.rstrip('/')}/v1/models"
    anthropic_version = os.getenv("ANTHROPIC_VERSION", "2023-06-01")

    try:
        resp = requests.get(
            url,
            headers={
                "x-api-key": api_key,
                "anthropic-version": anthropic_version,
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json().get("data", [])
        models = sorted({m.get("id", "") for m in data if m.get("id")})
        return models, None
    except Exception as e:
        # Fallback to known Claude models if API fails
        return [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
        ], None


def _list_watsonx_models(settings: AppSettings) -> Tuple[List[str], Optional[str]]:
    """
    List foundation models from Watsonx public specs endpoint.
    Returns a unique sorted list of model_id's across major regions.
    """
    all_models = set()

    for base in WATSONX_BASE_URLS:
        url = f"{base}{WATSONX_ENDPOINT}"
        try:
            resp = requests.get(url, params=WATSONX_PARAMS, timeout=10)
            resp.raise_for_status()
            resources = resp.json().get("resources", [])
            for m in resources:
                if _is_deprecated_or_withdrawn(m.get("lifecycle", [])):
                    continue
                model_id = m.get("model_id")
                # Filter for text-generation and vision models
                if model_id and any(
                    x in model_id.lower()
                    for x in ["llama", "granite", "mistral", "mixtral"]
                ):
                    all_models.add(model_id)
        except Exception:
            # Just skip this region on error
            continue

    if not all_models:
        # Fallback to known models
        return [
            "ibm/granite-3-8b-instruct",
            "meta-llama/llama-3-1-70b-instruct",
            "mistralai/mixtral-8x7b-instruct-v01",
        ], None

    return sorted(all_models), None


def _list_ollama_models(settings: AppSettings) -> Tuple[List[str], Optional[str]]:
    """
    List models from a local/remote Ollama server via /api/tags.
    """
    base_url = settings.ollama.base_url
    url = f"{base_url.rstrip('/')}/api/tags"

    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json().get("models", [])
        models = sorted({m.get("name", "") for m in data if m.get("name")})
        return models, None
    except Exception as e:
        return [], f"Error listing Ollama models from {url}: {e}"


# --- Public API ---


def list_models_for_provider(
    provider: LLMProvider,
    settings: Optional[AppSettings] = None,
) -> Tuple[List[str], Optional[str]]:
    """
    Return (models, error) for a given provider.

    Args:
        provider: The LLM provider to query
        settings: Optional settings instance

    Returns:
        Tuple of (models, error):
            - models: list of strings (model IDs / names)
            - error: human-readable error if something went wrong, otherwise None
    """
    if settings is None:
        settings = get_settings()

    if provider == LLMProvider.chimera:
        return _list_chimera_server_models(settings)
    if provider == LLMProvider.openai:
        return _list_openai_models(settings)
    if provider == LLMProvider.claude:
        return _list_claude_models(settings)
    if provider == LLMProvider.watsonx:
        return _list_watsonx_models(settings)
    if provider == LLMProvider.ollama:
        return _list_ollama_models(settings)

    return [], f"Unsupported provider: {provider}"


def list_all_providers_models(
    settings: Optional[AppSettings] = None,
) -> Dict[str, Tuple[List[str], Optional[str]]]:
    """
    List models for all providers.

    Args:
        settings: Optional settings instance

    Returns:
        Dict mapping provider name to (models, error) tuple
    """
    if settings is None:
        settings = get_settings()

    results = {}
    for provider in LLMProvider:
        models, error = list_models_for_provider(provider, settings)
        results[provider.value] = (models, error)

    return results


def get_recommended_models_by_task() -> Dict[str, List[str]]:
    """
    Return recommended models grouped by task type.

    Returns:
        Dict mapping task types to recommended models
    """
    return {
        "vision_analysis": [
            "gpt-4o",
            "gpt-4o-mini",
            "claude-3-5-sonnet-20241022",
            "llava:latest",
            "llava:13b",
            "bakllava",
        ],
        "code_assistance": [
            "gpt-4o",
            "claude-3-5-sonnet-20241022",
            "ibm/granite-3-8b-instruct",
            "deepseek-coder:latest",
        ],
        "general_assistant": [
            "gpt-4o-mini",
            "claude-3-5-haiku-20241022",
            "llama3.2:latest",
            "gemma:2b",
        ],
        "fast_local": [
            "llava:latest",
            "gemma:2b",
            "qwen2:1.5b",
            "phi3:mini",
        ],
    }
