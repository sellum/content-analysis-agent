#!/usr/bin/env python3
"""
Simple test script to verify the Content Analysis Agent works.
This tests the agent directly without HTTP overhead.
"""

import asyncio
from dapr_agents import tool, Agent, OpenAIChatClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@tool
def extract_themes(content: str) -> list:
    """Extract key themes and topics from the given content."""
    return ["AI", "technology", "innovation"]


@tool
def analyze_sentiment(content: str) -> dict:
    """Analyze the emotional tone and sentiment of the content."""
    return {"sentiment": "positive", "confidence": "high"}


@tool
def generate_summary(content: str) -> str:
    """Generate a concise summary of the content."""
    return "This content discusses technological advancement and innovation."


async def main():
    """Test the agent directly."""
    
    # Create a simple agent (not DurableAgent for this test)
    agent = Agent(
        name="TestAnalyzer",
        role="Test Content Analyst",
        instructions=[
            "You are a test content analyst.",
            "Use the provided tools to analyze content.",
            "Provide clear and concise analysis."
        ],
        tools=[extract_themes, analyze_sentiment, generate_summary],
        llm=OpenAIChatClient(model="gpt-3.5-turbo"),
    )
    
    test_content = "Artificial Intelligence is transforming industries and creating new opportunities."
    
    print("🧪 Testing Content Analysis Agent")
    print("=" * 50)
    print(f"Content: {test_content}")
    print()
    
    try:
        # Test the agent
        response = await agent.run(f"""
        Please analyze this content:
        
        {test_content}
        
        Use the available tools to:
        1. Extract themes using extract_themes
        2. Analyze sentiment using analyze_sentiment  
        3. Generate a summary using generate_summary
        
        Provide a comprehensive analysis.
        """)
        
        print("✅ Agent response:")
        print(response)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
