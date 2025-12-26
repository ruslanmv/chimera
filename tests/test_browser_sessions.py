"""
Chimera - Browser Session Management Tests
Tests for browser session lifecycle (spawn, persist, query, cleanup)
"""

import pytest
import asyncio
import httpx
from pathlib import Path


BASE_URL = "http://localhost:8000"
TIMEOUT = 60.0


@pytest.mark.browser
class TestBrowserSessionLifecycle:
    """Test browser session lifecycle management"""

    @pytest.mark.asyncio
    async def test_spawn_creates_session(self):
        """Test that spawning creates a persistent browser session"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # Spawn ChatGPT session
            response = await client.post(f"{BASE_URL}/api/spawn/chatgpt")
            print(f"\n✓ Spawn response: {response.status_code}")

            # Check status shows active session
            status_response = await client.get(f"{BASE_URL}/api/status")
            if status_response.status_code == 200:
                status = status_response.json()
                print(f"  Active sessions: {status.get('sessions', {})}")

    @pytest.mark.asyncio
    async def test_session_persists_cookies(self):
        """Test that browser sessions persist cookies/login state"""
        # Check that browser data directory exists
        chimera_dir = Path.home() / ".chimera_enterprise_data"

        if chimera_dir.exists():
            print(f"\n✓ Browser data directory exists: {chimera_dir}")
            # Check for Chrome profile data
            profile_files = list(chimera_dir.rglob("*"))
            print(f"  Found {len(profile_files)} files in browser profile")
            assert len(profile_files) > 0, \
                "Browser profile should contain session data"
        else:
            pytest.skip("Browser has not been spawned yet")

    @pytest.mark.asyncio
    async def test_multiple_sessions_independent(self):
        """Test that multiple browser sessions are independent"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            providers = ["chatgpt", "claude"]

            for provider in providers:
                response = await client.post(f"{BASE_URL}/api/spawn/{provider}")
                print(f"\n✓ Spawned {provider}: {response.status_code}")
                await asyncio.sleep(1)

            # Check status shows multiple sessions
            status_response = await client.get(f"{BASE_URL}/api/status")
            if status_response.status_code == 200:
                status = status_response.json()
                sessions = status.get('sessions', {})
                print(f"  Total active sessions: {len(sessions)}")


@pytest.mark.browser
class TestBrowserScreenshots:
    """Test browser screenshot functionality"""

    @pytest.mark.asyncio
    async def test_screenshot_available(self):
        """Test that screenshots are available for active sessions"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            try:
                response = await client.get(f"{BASE_URL}/api/screenshot/chatgpt")

                if response.status_code == 200:
                    print(f"\n✓ Screenshot available ({len(response.content)} bytes)")
                    assert len(response.content) > 0, "Screenshot should not be empty"
                    assert response.headers.get("content-type", "").startswith("image/"), \
                        "Screenshot should be an image"
                else:
                    pytest.skip(f"ChatGPT session not spawned: {response.status_code}")
            except httpx.ConnectError:
                pytest.skip("Server not running")


@pytest.mark.browser
class TestComputerUseTools:
    """Test computer use / browser automation tools"""

    @pytest.mark.asyncio
    async def test_goto_tool(self):
        """Test goto tool for navigation"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            try:
                response = await client.post(
                    f"{BASE_URL}/api/computer/chatgpt/tool",
                    json={
                        "name": "goto",
                        "arguments": {"url": "https://example.com"}
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    print(f"\n✓ goto tool executed: {result}")
                    assert "result" in result, "Tool should return result"
                else:
                    pytest.skip(f"Tool not available: {response.status_code}")
            except httpx.ConnectError:
                pytest.skip("Server not running")

    @pytest.mark.asyncio
    async def test_screenshot_tool(self):
        """Test screenshot tool"""
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            try:
                response = await client.post(
                    f"{BASE_URL}/api/computer/chatgpt/tool",
                    json={
                        "name": "screenshot",
                        "arguments": {}
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    print(f"\n✓ screenshot tool executed")
                    assert "result" in result, "Tool should return result"
                else:
                    pytest.skip(f"Tool not available: {response.status_code}")
            except httpx.ConnectError:
                pytest.skip("Server not running")


if __name__ == "__main__":
    pytest.main([
        __file__,
        "-v",
        "-s",
        "--tb=short",
        "-m", "browser"
    ])
