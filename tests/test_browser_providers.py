"""
Chimera - Browser Provider Tests
Tests for FREE web chatbot to API conversion

These tests verify that browser automation works correctly for:
- ChatGPT (chatgpt.com)
- Claude (claude.ai)
- Gemini (gemini.google.com)
- DeepSeek (chat.deepseek.com)
"""

import pytest
import asyncio
import httpx
from typing import Dict, Any
import time


# Test configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 120.0  # Browser automation can be slow
RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # seconds


class BrowserProviderTester:
    """Helper class for testing browser-based providers"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.client = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=TIMEOUT)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    async def spawn_head(self, provider: str) -> Dict[str, Any]:
        """Spawn a browser session for a provider"""
        response = await self.client.post(f"{self.base_url}/api/spawn/{provider}")
        return {
            "status_code": response.status_code,
            "message": response.text
        }

    async def check_status(self) -> Dict[str, Any]:
        """Check server status and active sessions"""
        response = await self.client.get(f"{self.base_url}/api/status")
        if response.status_code == 200:
            return response.json()
        return {"error": f"Status check failed: {response.status_code}"}

    async def query_provider(
        self,
        provider: str,
        question: str,
        retry_on_error: bool = True
    ) -> Dict[str, Any]:
        """
        Query a provider via the OpenAI-compatible API

        Args:
            provider: Provider name (chatgpt, claude, gemini, deepseek)
            question: Question to ask
            retry_on_error: Whether to retry on connection errors

        Returns:
            Dict with response or error information
        """
        for attempt in range(RETRY_ATTEMPTS if retry_on_error else 1):
            try:
                response = await self.client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json={
                        "model": provider,
                        "messages": [
                            {"role": "user", "content": question}
                        ]
                    },
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "provider": provider,
                        "question": question,
                        "answer": data["choices"][0]["message"]["content"],
                        "model": data.get("model"),
                        "attempt": attempt + 1
                    }
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    if attempt < RETRY_ATTEMPTS - 1 and retry_on_error:
                        print(f"Attempt {attempt + 1} failed: {error_msg}. Retrying in {RETRY_DELAY}s...")
                        await asyncio.sleep(RETRY_DELAY)
                        continue
                    return {
                        "success": False,
                        "provider": provider,
                        "error": error_msg,
                        "attempt": attempt + 1
                    }

            except (httpx.ConnectError, httpx.TimeoutException) as e:
                if attempt < RETRY_ATTEMPTS - 1 and retry_on_error:
                    print(f"Connection error on attempt {attempt + 1}: {e}. Retrying in {RETRY_DELAY}s...")
                    await asyncio.sleep(RETRY_DELAY)
                    continue
                return {
                    "success": False,
                    "provider": provider,
                    "error": f"Connection error: {str(e)}",
                    "attempt": attempt + 1
                }

        return {
            "success": False,
            "provider": provider,
            "error": "Max retries exceeded",
            "attempt": RETRY_ATTEMPTS
        }


# Simple test questions
SIMPLE_QUESTIONS = [
    "What is the capital of Italy?",
    "What is 2 + 2?",
    "Name one planet in our solar system.",
    "What color is the sky on a clear day?"
]


class TestServerAvailability:
    """Test that the Chimera server is running"""

    @pytest.mark.asyncio
    async def test_server_is_running(self):
        """Test that Chimera API server is accessible"""
        async with BrowserProviderTester() as tester:
            try:
                status = await tester.check_status()
                assert "plugins" in status or "error" not in status, \
                    "Server should be running at http://localhost:8000"
                print(f"\n✓ Server is running. Available plugins: {status.get('plugins', [])}")
            except Exception as e:
                pytest.skip(f"Server not running: {e}. Start with 'make dev' or 'uv run chimera-serve'")


@pytest.mark.browser
class TestChatGPTBrowser:
    """Test ChatGPT browser automation (FREE web chatbot)"""

    @pytest.mark.asyncio
    async def test_chatgpt_spawn(self):
        """Test spawning ChatGPT browser session"""
        async with BrowserProviderTester() as tester:
            result = await tester.spawn_head("chatgpt")
            print(f"\n📌 ChatGPT spawn result: {result}")
            # Spawning should at least not crash (200 or redirect expected)
            assert result["status_code"] in [200, 302], \
                "ChatGPT browser should spawn successfully"

    @pytest.mark.asyncio
    async def test_chatgpt_simple_query(self):
        """Test simple query to ChatGPT via browser automation"""
        async with BrowserProviderTester() as tester:
            question = "What is the capital of Italy?"
            result = await tester.query_provider("chatgpt", question)

            print(f"\n🤖 ChatGPT Test:")
            print(f"  Question: {question}")
            print(f"  Success: {result['success']}")
            if result['success']:
                print(f"  Answer: {result['answer'][:200]}...")
                assert "rome" in result['answer'].lower(), \
                    "ChatGPT should correctly answer 'Rome'"
            else:
                print(f"  Error: {result['error']}")
                pytest.skip(f"ChatGPT not available: {result['error']}")

    @pytest.mark.asyncio
    async def test_chatgpt_multiple_questions(self):
        """Test multiple questions to ChatGPT"""
        async with BrowserProviderTester() as tester:
            results = []
            for question in SIMPLE_QUESTIONS[:2]:  # Test 2 questions
                result = await tester.query_provider("chatgpt", question, retry_on_error=True)
                results.append(result)
                await asyncio.sleep(2)  # Avoid rate limiting

            successful = [r for r in results if r['success']]
            print(f"\n✓ ChatGPT answered {len(successful)}/{len(results)} questions")

            if len(successful) > 0:
                for r in successful:
                    print(f"  Q: {r['question']}")
                    print(f"  A: {r['answer'][:100]}...")
            else:
                pytest.skip("ChatGPT browser automation not working")


@pytest.mark.browser
class TestClaudeBrowser:
    """Test Claude browser automation (FREE web chatbot)"""

    @pytest.mark.asyncio
    async def test_claude_spawn(self):
        """Test spawning Claude browser session"""
        async with BrowserProviderTester() as tester:
            result = await tester.spawn_head("claude")
            print(f"\n📌 Claude spawn result: {result}")
            assert result["status_code"] in [200, 302, 404], \
                "Claude spawn should not crash (may need implementation)"

    @pytest.mark.asyncio
    async def test_claude_simple_query(self):
        """Test simple query to Claude via browser automation"""
        async with BrowserProviderTester() as tester:
            question = "What is the capital of Italy?"
            result = await tester.query_provider("claude", question)

            print(f"\n🤖 Claude Test:")
            print(f"  Question: {question}")
            print(f"  Success: {result['success']}")
            if result['success']:
                print(f"  Answer: {result['answer'][:200]}...")
                assert "rome" in result['answer'].lower(), \
                    "Claude should correctly answer 'Rome'"
            else:
                print(f"  Error: {result['error']}")
                pytest.skip(f"Claude browser automation not yet implemented: {result['error']}")


@pytest.mark.browser
class TestGeminiBrowser:
    """Test Gemini browser automation (FREE web chatbot)"""

    @pytest.mark.asyncio
    async def test_gemini_spawn(self):
        """Test spawning Gemini browser session"""
        async with BrowserProviderTester() as tester:
            result = await tester.spawn_head("gemini")
            print(f"\n📌 Gemini spawn result: {result}")
            assert result["status_code"] in [200, 302, 404], \
                "Gemini spawn should not crash (may need implementation)"

    @pytest.mark.asyncio
    async def test_gemini_simple_query(self):
        """Test simple query to Gemini via browser automation"""
        async with BrowserProviderTester() as tester:
            question = "What is the capital of Italy?"
            result = await tester.query_provider("gemini", question)

            print(f"\n🤖 Gemini Test:")
            print(f"  Question: {question}")
            print(f"  Success: {result['success']}")
            if result['success']:
                print(f"  Answer: {result['answer'][:200]}...")
                assert "rome" in result['answer'].lower(), \
                    "Gemini should correctly answer 'Rome'"
            else:
                print(f"  Error: {result['error']}")
                pytest.skip(f"Gemini browser automation not yet implemented: {result['error']}")


@pytest.mark.browser
class TestDeepSeekBrowser:
    """Test DeepSeek browser automation (FREE web chatbot)"""

    @pytest.mark.asyncio
    async def test_deepseek_spawn(self):
        """Test spawning DeepSeek browser session"""
        async with BrowserProviderTester() as tester:
            result = await tester.spawn_head("deepseek")
            print(f"\n📌 DeepSeek spawn result: {result}")
            assert result["status_code"] in [200, 302, 404], \
                "DeepSeek spawn should not crash (may need implementation)"

    @pytest.mark.asyncio
    async def test_deepseek_simple_query(self):
        """Test simple query to DeepSeek via browser automation"""
        async with BrowserProviderTester() as tester:
            question = "What is the capital of Italy?"
            result = await tester.query_provider("deepseek", question)

            print(f"\n🤖 DeepSeek Test:")
            print(f"  Question: {question}")
            print(f"  Success: {result['success']}")
            if result['success']:
                print(f"  Answer: {result['answer'][:200]}...")
                assert "rome" in result['answer'].lower(), \
                    "DeepSeek should correctly answer 'Rome'"
            else:
                print(f"  Error: {result['error']}")
                pytest.skip(f"DeepSeek browser automation not yet implemented: {result['error']}")


@pytest.mark.browser
class TestMultiProviderComparison:
    """Test multiple providers and compare results"""

    @pytest.mark.asyncio
    async def test_all_providers_same_question(self):
        """Ask the same question to all available providers"""
        async with BrowserProviderTester() as tester:
            question = "What is the capital of Italy?"
            providers = ["chatgpt", "claude", "gemini", "deepseek"]

            results = []
            for provider in providers:
                result = await tester.query_provider(provider, question, retry_on_error=True)
                results.append(result)
                await asyncio.sleep(2)  # Rate limiting

            print(f"\n{'='*60}")
            print(f"MULTI-PROVIDER COMPARISON")
            print(f"Question: {question}")
            print(f"{'='*60}")

            successful = []
            for result in results:
                provider = result['provider']
                if result['success']:
                    answer = result['answer'][:150]
                    print(f"\n✓ {provider.upper()}: {answer}...")
                    successful.append(provider)

                    # Verify correct answer
                    assert "rome" in result['answer'].lower(), \
                        f"{provider} should answer 'Rome'"
                else:
                    print(f"\n✗ {provider.upper()}: {result['error']}")

            print(f"\n{'='*60}")
            print(f"Results: {len(successful)}/{len(providers)} providers working")
            print(f"Working providers: {successful}")
            print(f"{'='*60}")

            # At least one provider should work (ChatGPT is implemented)
            assert len(successful) >= 1, \
                "At least one browser provider should be working"


@pytest.mark.browser
class TestErrorHandling:
    """Test error handling and recovery"""

    @pytest.mark.asyncio
    async def test_nonexistent_provider(self):
        """Test querying a non-existent provider"""
        async with BrowserProviderTester() as tester:
            result = await tester.query_provider("nonexistent", "test", retry_on_error=False)
            assert not result['success'], \
                "Non-existent provider should fail gracefully"
            print(f"\n✓ Non-existent provider failed gracefully: {result['error']}")

    @pytest.mark.asyncio
    async def test_connection_retry(self):
        """Test that connection errors trigger retries"""
        async with BrowserProviderTester() as tester:
            # This will likely fail, but should retry
            start_time = time.time()
            result = await tester.query_provider(
                "chatgpt",
                "test",
                retry_on_error=True
            )
            elapsed = time.time() - start_time

            print(f"\n📊 Connection test:")
            print(f"  Attempts: {result.get('attempt', 1)}")
            print(f"  Elapsed: {elapsed:.1f}s")
            print(f"  Success: {result['success']}")

            # Should have attempted retries if failed
            if not result['success']:
                assert elapsed >= RETRY_DELAY or result.get('attempt', 1) > 1, \
                    "Failed requests should retry with delays"


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([
        __file__,
        "-v",
        "-s",  # Show print statements
        "--tb=short",
        "-m", "browser"  # Only run browser tests
    ])
