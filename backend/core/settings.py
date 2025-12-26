"""
Chimera Settings and Configuration Management
Enterprise-grade configuration with multiple LLM providers
"""

from __future__ import annotations

import os
from enum import Enum
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProvider(str, Enum):
    """Supported LLM providers"""

    chimera = "chimera"  # Default managed server
    openai = "openai"
    claude = "claude"
    watsonx = "watsonx"
    ollama = "ollama"


class OpenAISettings(BaseSettings):
    """OpenAI configuration"""

    model_config = SettingsConfigDict(env_prefix="OPENAI_", case_sensitive=False)

    api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    model: str = Field(default="gpt-4o", description="OpenAI model to use")
    base_url: Optional[str] = Field(default=None, description="Custom API base URL")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=1)


class ClaudeSettings(BaseSettings):
    """Anthropic Claude configuration"""

    model_config = SettingsConfigDict(env_prefix="ANTHROPIC_", case_sensitive=False)

    api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    model: str = Field(default="claude-3-5-sonnet-20241022", description="Claude model to use")
    base_url: Optional[str] = Field(default=None, description="Custom API base URL")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=2048, ge=1)


class WatsonxSettings(BaseSettings):
    """IBM Watsonx configuration"""

    model_config = SettingsConfigDict(env_prefix="WATSONX_", case_sensitive=False)

    api_key: Optional[str] = Field(default=None, description="Watsonx API key")
    project_id: Optional[str] = Field(default=None, description="Watsonx project ID")
    model_id: str = Field(
        default="ibm/granite-3-8b-instruct", description="Watsonx model ID"
    )
    base_url: str = Field(
        default="https://us-south.ml.cloud.ibm.com", description="Watsonx base URL"
    )
    temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1)


class OllamaSettings(BaseSettings):
    """Ollama local models configuration"""

    model_config = SettingsConfigDict(env_prefix="OLLAMA_", case_sensitive=False)

    model: str = Field(default="llava:latest", description="Ollama model to use")
    base_url: str = Field(
        default="http://localhost:11434", description="Ollama server URL"
    )
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    timeout: int = Field(default=120, description="Request timeout in seconds")


class ChimeraServerSettings(BaseSettings):
    """Chimera managed server configuration"""

    model_config = SettingsConfigDict(env_prefix="CHIMERA_SERVER_", case_sensitive=False)

    api_url: str = Field(
        default="https://api.chimera-ai.com/v1", description="Chimera server API URL"
    )
    api_key: Optional[str] = Field(default=None, description="Chimera server API key")
    model: str = Field(default="chimera-vision-1", description="Chimera model to use")


class AppSettings(BaseSettings):
    """Main application settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General settings
    app_name: str = Field(default="Chimera Desktop Assistant", description="Application name")
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    # Default provider
    provider: LLMProvider = Field(
        default=LLMProvider.chimera,
        description="Active LLM provider",
        env="CHIMERA_DEFAULT_PROVIDER",
    )

    # Privacy settings
    store_screenshots: bool = Field(
        default=False, description="Store screenshots on server"
    )
    analytics_enabled: bool = Field(default=False, description="Enable analytics")

    # Provider configurations
    chimera_server: ChimeraServerSettings = Field(default_factory=ChimeraServerSettings)
    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    claude: ClaudeSettings = Field(default_factory=ClaudeSettings)
    watsonx: WatsonxSettings = Field(default_factory=WatsonxSettings)
    ollama: OllamaSettings = Field(default_factory=OllamaSettings)

    # Server settings
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, ge=1, le=65535, description="Server port")
    reload: bool = Field(default=False, description="Enable auto-reload")

    # Feature flags
    enable_monitoring: bool = Field(default=True, description="Enable monitoring features")
    enable_multi_monitor: bool = Field(
        default=True, description="Enable multi-monitor support"
    )


# Singleton instance
_settings: Optional[AppSettings] = None


def get_settings() -> AppSettings:
    """Get or create settings singleton"""
    global _settings
    if _settings is None:
        _settings = AppSettings()
    return _settings


def reload_settings() -> AppSettings:
    """Reload settings from environment/config files"""
    global _settings
    _settings = AppSettings()
    return _settings
