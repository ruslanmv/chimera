"""
Chimera Enterprise - Provider Comparison
Compare responses from different LLM providers side-by-side
"""

import asyncio
import httpx
from typing import List, Dict
import time


class ProviderComparison:
    """Compare responses from multiple LLM providers"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)

    async def compare_providers(
        self,
        prompt: str,
        providers: List[Dict[str, str]]
    ) -> Dict[str, Dict]:
        """
        Compare responses from multiple providers

        Args:
            prompt: Question/prompt to ask all providers
            providers: List of {"name": "...", "model": "..."}

        Returns:
            Dict of provider responses with timing info
        """
        results = {}

        for provider_info in providers:
            provider = provider_info["name"]
            model = provider_info.get("model")

            print(f"\n🤖 Querying {provider.upper()}...")

            start_time = time.time()
            try:
                response = await self.client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json={
                        "model": model or f"{provider}-default",
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    headers={"X-Provider": provider}
                )

                elapsed = time.time() - start_time

                if response.status_code == 200:
                    data = response.json()
                    results[provider] = {
                        "response": data["choices"][0]["message"]["content"],
                        "model": data.get("model", model),
                        "time": f"{elapsed:.2f}s",
                        "tokens": data.get("usage", {}),
                        "status": "✓ Success"
                    }
                    print(f"✓ {provider.upper()} completed in {elapsed:.2f}s")
                else:
                    results[provider] = {
                        "response": None,
                        "error": response.text,
                        "time": f"{elapsed:.2f}s",
                        "status": "✗ Failed"
                    }
                    print(f"✗ {provider.upper()} failed")

            except Exception as e:
                elapsed = time.time() - start_time
                results[provider] = {
                    "response": None,
                    "error": str(e),
                    "time": f"{elapsed:.2f}s",
                    "status": "✗ Error"
                }
                print(f"✗ {provider.upper()} error: {e}")

        return results

    def print_comparison(self, results: Dict):
        """Pretty print comparison results"""
        print("\n" + "=" * 80)
        print("COMPARISON RESULTS")
        print("=" * 80)

        for provider, data in results.items():
            print(f"\n{'─' * 80}")
            print(f"🤖 PROVIDER: {provider.upper()}")
            print(f"{'─' * 80}")
            print(f"Status: {data['status']}")
            print(f"Time: {data['time']}")

            if data.get('model'):
                print(f"Model: {data['model']}")

            if data.get('tokens'):
                tokens = data['tokens']
                print(f"Tokens: {tokens.get('total_tokens', 'N/A')} total")

            if data.get('response'):
                print(f"\nResponse:\n{data['response'][:500]}")
                if len(data['response']) > 500:
                    print("\n... (truncated)")
            elif data.get('error'):
                print(f"\nError: {data['error']}")

        print(f"\n{'=' * 80}\n")

    async def close(self):
        await self.client.aclose()


async def main():
    """Run provider comparison examples"""
    comparison = ProviderComparison()

    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         CHIMERA ENTERPRISE - PROVIDER COMPARISON             ║
║                                                              ║
║  Compare ChatGPT, Claude, Gemini, Ollama & WatsonX           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    try:
        # Define providers to compare
        providers = [
            {"name": "ollama", "model": "deepseek-r1:latest"},
            {"name": "chatgpt", "model": "gpt-4-turbo"},
            {"name": "claude", "model": "claude-3-5-sonnet-20241022"},
            {"name": "gemini", "model": "gemini-2.0-flash-exp"},
            # Uncomment if WatsonX is configured:
            # {"name": "watsonx", "model": "ibm/granite-13b-chat-v2"}
        ]

        # Test Question
        prompt = """Explain quantum computing in simple terms suitable for
        a business executive. Focus on practical applications."""

        print(f"\n📝 Test Prompt:\n{prompt}\n")
        print(f"🔄 Comparing {len(providers)} providers...\n")

        # Run comparison
        results = await comparison.compare_providers(prompt, providers)

        # Print results
        comparison.print_comparison(results)

        # Summary
        successful = sum(1 for r in results.values() if r['status'] == '✓ Success')
        print(f"📊 Summary: {successful}/{len(providers)} providers responded successfully\n")

    finally:
        await comparison.close()


if __name__ == "__main__":
    asyncio.run(main())
