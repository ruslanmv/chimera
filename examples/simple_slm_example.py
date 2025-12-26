"""
Chimera Enterprise - Simple SLM (Small Language Model) Example
Demonstrates using local, lightweight models via Ollama
"""

import asyncio
import httpx


class SimpleSLMAgent:
    """
    Simple agent using Small Language Models (SLMs) for fast, local inference

    Benefits of SLMs:
    - Privacy (runs locally, no API calls)
    - Speed (faster inference)
    - Cost (no API fees)
    - Offline (works without internet)
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def query(self, prompt: str, model: str = "phi3:mini") -> str:
        """Query a small language model"""
        response = await self.client.post(
            f"{self.base_url}/v1/chat/completions",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}]
            },
            headers={"X-Provider": "ollama"}
        )

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Error: {response.text}")

    async def close(self):
        await self.client.aclose()


async def main():
    """Run SLM examples"""
    agent = SimpleSLMAgent()

    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       CHIMERA ENTERPRISE - SMALL LANGUAGE MODELS (SLMs)      ║
║                                                              ║
║  Fast, Local, Private AI with Phi-3, Gemma, Qwen, etc.      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    try:
        # Example 1: Simple Q&A
        print("\n📝 Example 1: Simple Question Answering")
        print("-" * 60)
        answer = await agent.query(
            "What is the capital of France?",
            model="phi3:mini"
        )
        print(f"Answer: {answer}\n")

        # Example 2: Code Generation
        print("\n💻 Example 2: Code Generation")
        print("-" * 60)
        code = await agent.query(
            "Write a Python function to calculate fibonacci numbers",
            model="qwen2.5-coder:latest"
        )
        print(f"Generated Code:\n{code}\n")

        # Example 3: Text Summarization
        print("\n📄 Example 3: Text Summarization")
        print("-" * 60)
        summary = await agent.query(
            """Summarize this text:
            Artificial intelligence is transforming enterprise software.
            Companies are adopting AI agents for automation, data analysis,
            and customer service. The key challenges are integration,
            governance, and ensuring AI alignment with business goals.
            """,
            model="gemma2:2b"
        )
        print(f"Summary: {summary}\n")

        # Example 4: Multi-lingual Support
        print("\n🌍 Example 4: Multi-lingual Support")
        print("-" * 60)
        translation = await agent.query(
            "Translate to Spanish: Hello, how can I help you today?",
            model="phi3:mini"
        )
        print(f"Translation: {translation}\n")

    finally:
        await agent.close()


if __name__ == "__main__":
    print("\n💡 TIP: Popular SLMs available via Ollama:")
    print("  - phi3:mini (3.8B params) - Microsoft's efficient model")
    print("  - gemma2:2b (2B params) - Google's lightweight model")
    print("  - qwen2.5-coder:latest - Specialized for code")
    print("  - deepseek-r1:latest - Advanced reasoning")
    print("\nInstall with: ollama pull <model-name>\n")

    asyncio.run(main())
