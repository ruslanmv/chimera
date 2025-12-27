"""
Lightweight unit tests for Eel Launcher
Simple tests to verify basic functionality
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.eel_launcher import ChimeraLauncher


class TestChimeraLauncher:
    """Basic test suite for ChimeraLauncher"""

    def test_launcher_initialization(self):
        """Test launcher initializes with correct defaults"""
        launcher = ChimeraLauncher()
        assert launcher.frontend_path == "frontend/dist"
        assert launcher.backend_port == 8000
        assert launcher.frontend_port == 8080

    def test_launcher_custom_ports(self):
        """Test launcher with custom ports"""
        launcher = ChimeraLauncher(backend_port=9000, frontend_port=9090)
        assert launcher.backend_port == 9000
        assert launcher.frontend_port == 9090


class TestSettings:
    """Basic settings configuration tests"""

    def test_gemini_settings_import(self):
        """Test that Gemini settings can be imported"""
        from backend.core.settings import GeminiSettings
        settings = GeminiSettings()
        assert settings.model == "gemini-2.0-flash-exp"

    def test_claude_settings_import(self):
        """Test that Claude settings can be imported"""
        from backend.core.settings import ClaudeSettings
        settings = ClaudeSettings()
        assert settings.model == "claude-3-5-sonnet-20241022"

    def test_llm_provider_enum(self):
        """Test LLM provider enum includes all providers"""
        from backend.core.settings import LLMProvider
        assert hasattr(LLMProvider, "gemini")
        assert hasattr(LLMProvider, "claude")
        assert hasattr(LLMProvider, "ollama")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
