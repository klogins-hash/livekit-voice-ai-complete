#!/usr/bin/env python3
"""
Test script for real RUBE MCP integration
This tests the actual RUBE MCP tools in the agent.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv

async def test_real_rube_integration():
    """Test the real RUBE MCP integration"""
    print("🧪 Testing Real RUBE MCP Integration")
    print("=" * 40)
    
    # Load environment
    load_dotenv(".env.local")
    
    # Check API key
    api_key = os.getenv("RUBE_API_KEY")
    if not api_key:
        print("❌ RUBE_API_KEY not found in environment")
        return False
    
    print(f"✅ RUBE API Key found: {api_key[:20]}...")
    
    # Test if we can access the RUBE MCP tools
    try:
        print("\n🔍 Testing RUBE_SEARCH_TOOLS access...")
        
        # Try to call the actual RUBE_SEARCH_TOOLS function
        result = await mcp0_rube__RUBE_SEARCH_TOOLS({
            "use_case": "send an email to test@example.com",
            "known_fields": "email:test@example.com",
            "session": {"generate_id": True}
        })
        
        print(f"✅ RUBE_SEARCH_TOOLS result: {result}")
        
        print("\n⚡ Testing RUBE_MULTI_EXECUTE_TOOL access...")
        
        # Try to call the actual RUBE_MULTI_EXECUTE_TOOL function
        execute_result = await mcp0_rube__RUBE_MULTI_EXECUTE_TOOL({
            "tools": [{"tool_slug": "GMAIL_SEND_EMAIL", "arguments": {"to": "test@example.com"}}],
            "memory": {},
            "session_id": "test-session",
            "sync_response_to_workbench": False,
            "thought": "Testing RUBE integration"
        })
        
        print(f"✅ RUBE_MULTI_EXECUTE_TOOL result: {execute_result}")
        
        print("\n🔗 Testing RUBE_MANAGE_CONNECTIONS access...")
        
        # Try to call the actual RUBE_MANAGE_CONNECTIONS function
        connection_result = await mcp0_rube__RUBE_MANAGE_CONNECTIONS({
            "toolkits": ["gmail", "slack"]
        })
        
        print(f"✅ RUBE_MANAGE_CONNECTIONS result: {connection_result}")
        
        print("\n🎉 Real RUBE MCP integration test completed successfully!")
        print("The agent can now actually call RUBE tools for real app automation!")
        return True
        
    except NameError as e:
        print(f"❌ RUBE MCP tools not available in this context: {e}")
        print("The agent needs to be run in an environment where RUBE MCP tools are accessible.")
        return False
    except Exception as e:
        print(f"❌ Error testing RUBE MCP integration: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_real_rube_integration())
