"""
Pytest configuration and fixtures for Chimera tests
"""

import pytest
import asyncio
import httpx
import sys
from pathlib import Path

# Add backend to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def event_loop():
    """Create an event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def http_client():
    """Provide an HTTP client for API tests"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        yield client


@pytest.fixture
def server_url():
    """Provide the server URL"""
    return "http://localhost:8000"


@pytest.fixture
async def check_server_running(server_url):
    """Check if Chimera server is running"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{server_url}/api/status")
            return response.status_code == 200
    except (httpx.ConnectError, httpx.TimeoutException):
        return False


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "browser: mark test as browser automation test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Add asyncio marker to all async tests automatically
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asyncio)


@pytest.fixture(scope="session")
def test_questions():
    """Standard test questions for provider testing"""
    return [
        {
            "question": "What is the capital of Italy?",
            "expected_keyword": "rome",
            "category": "geography"
        },
        {
            "question": "What is 2 + 2?",
            "expected_keyword": "4",
            "category": "math"
        },
        {
            "question": "Name one planet in our solar system.",
            "expected_keywords": ["earth", "mars", "venus", "jupiter", "saturn", "mercury", "uranus", "neptune"],
            "category": "science"
        },
        {
            "question": "What color is the sky on a clear day?",
            "expected_keyword": "blue",
            "category": "general"
        }
    ]


@pytest.fixture
def simple_question():
    """Provide a simple test question"""
    return "What is the capital of Italy?"


@pytest.fixture
def expected_answer():
    """Provide expected answer for simple question"""
    return "rome"
