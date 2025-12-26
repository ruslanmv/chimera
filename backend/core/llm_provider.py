"""
Chimera LLM Provider
Unified interface for multiple LLM providers with CrewAI integration
"""

from __future__ import annotations

import os
from typing import Optional

from crewai import LLM

from .settings import AppSettings, LLMProvider, get_settings


class LLMProviderError(Exception):
    """Base exception for LLM provider errors"""

    pass


def build_llm(settings: Optional[AppSettings] = None) -> LLM:
    """
    Build and return an initialized CrewAI LLM using the active provider.

    Args:
        settings: Optional AppSettings instance. If None, uses get_settings().

    Returns:
        Configured CrewAI LLM instance

    Raises:
        LLMProviderError: If provider configuration is invalid
        ValueError: If provider is not supported
    """
    if settings is None:
        settings = get_settings()

    provider = settings.provider

    if provider == LLMProvider.chimera:
        return _build_chimera_server_llm(settings)

    if provider == LLMProvider.openai:
        return _build_openai_llm(settings)

    if provider == LLMProvider.claude:
        return _build_claude_llm(settings)

    if provider == LLMProvider.watsonx:
        return _build_watsonx_llm(settings)

    if provider == LLMProvider.ollama:
        return _build_ollama_llm(settings)

    raise ValueError(f"Unsupported provider: {provider}")


def _build_chimera_server_llm(settings: AppSettings) -> LLM:
    """Build LLM for Chimera managed server"""
    api_key = settings.chimera_server.api_key or os.getenv("CHIMERA_SERVER_API_KEY")

    # Chimera server doesn't require API key for basic usage
    # but may require it for higher rate limits
    model = f"chimera/{settings.chimera_server.model}"

    return LLM(
        model=model,
        base_url=settings.chimera_server.api_url,
        api_key=api_key or "not-required",
    )


def _build_openai_llm(settings: AppSettings) -> LLM:
    """Build LLM for OpenAI"""
    api_key = settings.openai.api_key or os.getenv("OPENAI_API_KEY", "")
    model = settings.openai.model
    base_url = settings.openai.base_url or os.getenv("OPENAI_BASE_URL", "")

    # Validate required credentials
    if not api_key:
        raise LLMProviderError(
            "OpenAI API key is required. "
            "Set OPENAI_API_KEY environment variable or configure in settings."
        )

    # Ensure model has provider prefix for CrewAI
    if not model.startswith("openai/"):
        model = f"openai/{model}"

    kwargs = {
        "model": model,
        "api_key": api_key,
        "temperature": settings.openai.temperature,
        "max_tokens": settings.openai.max_tokens,
    }

    if base_url:
        kwargs["base_url"] = base_url

    return LLM(**kwargs)


def _build_claude_llm(settings: AppSettings) -> LLM:
    """Build LLM for Anthropic Claude"""
    api_key = settings.claude.api_key or os.getenv("ANTHROPIC_API_KEY", "")
    model = settings.claude.model
    base_url = settings.claude.base_url or os.getenv("ANTHROPIC_BASE_URL", "")

    # Validate required credentials
    if not api_key:
        raise LLMProviderError(
            "Claude (Anthropic) API key is required. "
            "Set ANTHROPIC_API_KEY environment variable or configure in settings."
        )

    # CRITICAL: Set API key as environment variable (required by CrewAI's Anthropic provider)
    os.environ["ANTHROPIC_API_KEY"] = api_key

    if base_url:
        os.environ["ANTHROPIC_BASE_URL"] = base_url

    # Ensure model has provider prefix for CrewAI
    if not model.startswith("anthropic/"):
        model = f"anthropic/{model}"

    kwargs = {
        "model": model,
        "api_key": api_key,
        "temperature": settings.claude.temperature,
        "max_tokens": settings.claude.max_tokens,
    }

    if base_url:
        kwargs["base_url"] = base_url

    return LLM(**kwargs)


def _build_watsonx_llm(settings: AppSettings) -> LLM:
    """Build LLM for IBM Watsonx"""
    api_key = settings.watsonx.api_key or os.getenv("WATSONX_API_KEY", "")
    project_id = settings.watsonx.project_id or os.getenv("WATSONX_PROJECT_ID", "")
    model = settings.watsonx.model_id
    base_url = settings.watsonx.base_url

    # Validate required credentials
    if not api_key:
        raise LLMProviderError(
            "Watsonx API key is required. "
            "Set WATSONX_API_KEY environment variable or configure in settings."
        )
    if not project_id:
        raise LLMProviderError(
            "Watsonx project ID is required. "
            "Set WATSONX_PROJECT_ID environment variable or configure in settings."
        )

    # CRITICAL: Set environment variables (required by watsonx.ai SDK)
    os.environ["WATSONX_PROJECT_ID"] = project_id
    os.environ["WATSONX_URL"] = base_url

    # Ensure model has provider prefix for CrewAI
    # Format: watsonx/provider/model
    if not model.startswith("watsonx/"):
        model = f"watsonx/{model}"

    return LLM(
        model=model,
        api_key=api_key,
        base_url=base_url,
        project_id=project_id,
        temperature=settings.watsonx.temperature,
        max_tokens=settings.watsonx.max_tokens,
    )


def _build_ollama_llm(settings: AppSettings) -> LLM:
    """Build LLM for Ollama (local models)"""
    model = settings.ollama.model
    base_url = settings.ollama.base_url

    # Validate configuration
    if not base_url:
        raise LLMProviderError(
            "Ollama base URL is required. "
            "Set OLLAMA_BASE_URL environment variable or configure in settings."
        )

    # Ensure model has provider prefix for CrewAI
    if not model.startswith("ollama/"):
        model = f"ollama/{model}"

    return LLM(
        model=model,
        base_url=base_url,
        temperature=settings.ollama.temperature,
        timeout=settings.ollama.timeout,
    )


# Singleton LLM instance (lazy loaded)
_llm_instance: Optional[LLM] = None


def get_llm(reload: bool = False) -> LLM:
    """
    Get or create singleton LLM instance.

    Args:
        reload: If True, rebuild the LLM instance from current settings

    Returns:
        Configured LLM instance
    """
    global _llm_instance

    if reload or _llm_instance is None:
        _llm_instance = build_llm()

    return _llm_instance
