"""
Chimera Enterprise - Multi-Agent Workflow Example
Demonstrates orchestrating multiple LLM providers for complex tasks
"""

import asyncio
import httpx
from typing import List, Dict, Any


class MultiAgentOrchestrator:
    """
    Orchestrates multiple LLM providers for complex multi-step workflows

    Example workflow:
    1. ChatGPT (OpenAI) - Initial research and planning
    2. Claude (Anthropic) - Deep analysis and reasoning
    3. Gemini (Google) - Creative content generation
    4. Ollama (Local) - Fast iterations and refinements
    5. WatsonX (IBM) - Enterprise compliance checks
    """

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)

    async def query_provider(
        self,
        provider: str,
        messages: List[Dict[str, str]],
        model: str = None
    ) -> str:
        """Query a specific LLM provider"""
        payload = {
            "model": model or f"{provider}-default",
            "messages": messages
        }

        # Route through Chimera's unified API
        response = await self.client.post(
            f"{self.base_url}/v1/chat/completions",
            json=payload,
            headers={"X-Provider": provider}  # Custom header for provider routing
        )

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            raise Exception(f"{provider} error: {response.text}")

    async def research_task(self, topic: str) -> Dict[str, Any]:
        """
        Multi-agent research workflow

        Stage 1: ChatGPT does broad research
        Stage 2: Claude does deep analysis
        Stage 3: Gemini synthesizes insights
        Stage 4: Ollama formats final report
        """
        print(f"\n🔬 Multi-Agent Research: {topic}\n")

        # Stage 1: ChatGPT - Broad Research
        print("📊 Stage 1: ChatGPT performing broad research...")
        chatgpt_result = await self.query_provider(
            "chatgpt",
            [{"role": "user", "content": f"Research the topic: {topic}. Provide key facts and trends."}],
            model="gpt-4-turbo"
        )
        print(f"✓ ChatGPT completed\n")

        # Stage 2: Claude - Deep Analysis
        print("🧠 Stage 2: Claude performing deep analysis...")
        claude_result = await self.query_provider(
            "claude",
            [
                {"role": "user", "content": f"Based on this research:\n\n{chatgpt_result}\n\nProvide deep analysis and critical insights."}
            ],
            model="claude-3-5-sonnet-20241022"
        )
        print(f"✓ Claude completed\n")

        # Stage 3: Gemini - Creative Synthesis
        print("✨ Stage 3: Gemini synthesizing insights...")
        gemini_result = await self.query_provider(
            "gemini",
            [
                {"role": "user", "content": f"Synthesize these insights creatively:\n\nResearch: {chatgpt_result}\n\nAnalysis: {claude_result}"}
            ],
            model="gemini-2.0-flash-exp"
        )
        print(f"✓ Gemini completed\n")

        # Stage 4: Ollama - Local Formatting
        print("📝 Stage 4: Ollama formatting final report...")
        ollama_result = await self.query_provider(
            "ollama",
            [
                {"role": "user", "content": f"Format this into a professional report:\n\n{gemini_result}"}
            ],
            model="deepseek-r1:latest"
        )
        print(f"✓ Ollama completed\n")

        return {
            "topic": topic,
            "research": chatgpt_result,
            "analysis": claude_result,
            "synthesis": gemini_result,
            "final_report": ollama_result
        }

    async def code_review_workflow(self, code: str) -> Dict[str, Any]:
        """
        Multi-agent code review workflow

        Stage 1: Ollama - Fast syntax check
        Stage 2: Claude - Deep code analysis
        Stage 3: ChatGPT - Security review
        Stage 4: WatsonX - Enterprise compliance
        """
        print(f"\n🔍 Multi-Agent Code Review\n")

        # Stage 1: Ollama - Fast Check
        print("⚡ Stage 1: Ollama performing fast syntax check...")
        ollama_result = await self.query_provider(
            "ollama",
            [{"role": "user", "content": f"Quick syntax and style check:\n\n```\n{code}\n```"}]
        )
        print(f"✓ Ollama completed\n")

        # Stage 2: Claude - Deep Analysis
        print("🔬 Stage 2: Claude performing deep analysis...")
        claude_result = await self.query_provider(
            "claude",
            [{"role": "user", "content": f"Deep code analysis:\n\n```\n{code}\n```\n\nCheck: architecture, patterns, edge cases"}]
        )
        print(f"✓ Claude completed\n")

        # Stage 3: ChatGPT - Security
        print("🔐 Stage 3: ChatGPT performing security review...")
        chatgpt_result = await self.query_provider(
            "chatgpt",
            [{"role": "user", "content": f"Security vulnerability scan:\n\n```\n{code}\n```"}]
        )
        print(f"✓ ChatGPT completed\n")

        # Stage 4: WatsonX - Compliance
        print("📋 Stage 4: WatsonX checking enterprise compliance...")
        try:
            watsonx_result = await self.query_provider(
                "watsonx",
                [{"role": "user", "content": f"Enterprise compliance check:\n\n```\n{code}\n```"}]
            )
            print(f"✓ WatsonX completed\n")
        except Exception as e:
            watsonx_result = f"WatsonX unavailable: {e}"
            print(f"⚠ WatsonX skipped\n")

        return {
            "syntax_check": ollama_result,
            "deep_analysis": claude_result,
            "security_review": chatgpt_result,
            "compliance_check": watsonx_result
        }

    async def creative_collaboration(self, prompt: str) -> Dict[str, str]:
        """
        Creative multi-agent collaboration

        Each provider contributes its unique strengths:
        - Gemini: Creative ideation
        - Claude: Structured thinking
        - ChatGPT: Practical implementation
        - Ollama: Fast iteration
        """
        print(f"\n🎨 Multi-Agent Creative Collaboration\n")

        tasks = [
            ("gemini", "Generate creative ideas", "gemini-2.0-flash-exp"),
            ("claude", "Structure and refine", "claude-3-5-sonnet-20241022"),
            ("chatgpt", "Add practical details", "gpt-4-turbo"),
            ("ollama", "Final polish", "deepseek-r1:latest")
        ]

        results = {}
        context = prompt

        for provider, task, model in tasks:
            print(f"🤖 {provider.upper()}: {task}...")
            result = await self.query_provider(
                provider,
                [{"role": "user", "content": f"{context}\n\nTask: {task}"}],
                model=model
            )
            results[provider] = result
            context = result  # Each agent builds on previous work
            print(f"✓ {provider.upper()} completed\n")

        return results

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


async def main():
    """Run example workflows"""
    orchestrator = MultiAgentOrchestrator()

    try:
        # Example 1: Research Workflow
        print("=" * 60)
        print("EXAMPLE 1: MULTI-AGENT RESEARCH")
        print("=" * 60)
        research = await orchestrator.research_task(
            "The future of AI agents in enterprise software"
        )
        print("\n📄 Final Report Preview:")
        print(research["final_report"][:500] + "...\n")

        # Example 2: Code Review Workflow
        print("\n" + "=" * 60)
        print("EXAMPLE 2: MULTI-AGENT CODE REVIEW")
        print("=" * 60)
        sample_code = """
def process_payment(user_id, amount):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    return charge_card(amount)
        """
        review = await orchestrator.code_review_workflow(sample_code)
        print("\n🔍 Security Review Preview:")
        print(review["security_review"][:500] + "...\n")

        # Example 3: Creative Collaboration
        print("\n" + "=" * 60)
        print("EXAMPLE 3: CREATIVE COLLABORATION")
        print("=" * 60)
        creative = await orchestrator.creative_collaboration(
            "Design a revolutionary user interface for AI assistants"
        )
        print("\n✨ Final Result Preview:")
        print(creative["ollama"][:500] + "...\n")

    finally:
        await orchestrator.close()


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        CHIMERA ENTERPRISE - MULTI-AGENT WORKFLOWS            ║
║                                                              ║
║  Orchestrating ChatGPT, Claude, Gemini, Ollama & WatsonX     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    asyncio.run(main())
