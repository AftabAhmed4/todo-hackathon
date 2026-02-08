"""
Test script for OpenAI Agents SDK + Gemini integration.

Run this to verify your setup is working correctly.
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_agent():
    """Test the agent setup."""
    print("🧪 Testing OpenAI Agents SDK + Gemini Setup\n")

    # Check environment variables
    print("1. Checking environment variables...")
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        print("   ✓ GEMINI_API_KEY found")
    else:
        print("   ✗ GEMINI_API_KEY not found")
        return False

    # Check imports
    print("\n2. Checking dependencies...")
    try:
        from agents import Agent, Runner, function_tool
        print("   ✓ openai-agents installed")
    except ImportError as e:
        print(f"   ✗ openai-agents not installed: {e}")
        return False

    try:
        from agents.extensions.models.litellm_model import LitellmModel
        print("   ✓ litellm installed")
    except ImportError as e:
        print(f"   ✗ litellm not installed: {e}")
        return False

    try:
        import google.generativeai as genai
        print("   ✓ google-generativeai installed")
    except ImportError as e:
        print(f"   ✗ google-generativeai not installed: {e}")
        return False

    # Test agent creation
    print("\n3. Testing agent creation...")
    try:
        from agent_openai import get_gemini_agent
        agent = get_gemini_agent()
        print("   ✓ Agent created successfully")
        print(f"   - Agent name: {agent.name}")
        print(f"   - Number of tools: {len(agent.tools)}")
    except Exception as e:
        print(f"   ✗ Failed to create agent: {e}")
        return False

    # Test simple agent run (without database)
    print("\n4. Testing agent execution...")
    try:
        @function_tool
        def test_tool(message: str) -> str:
            """A simple test tool."""
            return f"Received: {message}"

        test_agent = Agent(
            name="Test Agent",
            instructions="You are a test assistant. Use the test_tool when asked.",
            model=LitellmModel(
                model="gemini/gemini-1.5-pro",
                api_key=gemini_key,
            ),
            tools=[test_tool],
        )

        result = await Runner.run(test_agent, "Say hello using the test tool")
        print("   ✓ Agent executed successfully")
        print(f"   - Response: {result.final_output[:100]}...")
    except Exception as e:
        print(f"   ✗ Failed to run agent: {e}")
        return False

    print("\n✅ All tests passed! Your setup is ready.")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_agent())
    if not success:
        print("\n❌ Setup incomplete. Please check the errors above.")
        exit(1)
