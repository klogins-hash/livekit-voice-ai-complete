#!/usr/bin/env python3
"""
Test script for RUBE MCP integration
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
from rube_integration import initialize_rube, get_rube_client

async def test_rube_integration():
    """Test the RUBE MCP integration"""
    print("🧪 Testing RUBE MCP Integration")
    print("=" * 40)
    
    # Load environment
    load_dotenv(".env.local")
    
    # Check API key
    api_key = os.getenv("RUBE_API_KEY")
    if not api_key:
        print("❌ RUBE_API_KEY not found in environment")
        return False
    
    print(f"✅ RUBE API Key found: {api_key[:20]}...")
    
    # Initialize RUBE client
    print("\n🔄 Initializing RUBE client...")
    success = await initialize_rube()
    
    if not success:
        print("❌ RUBE initialization failed")
        return False
    
    print("✅ RUBE client initialized successfully")
    
    # Test tool search
    print("\n🔍 Testing tool search...")
    client = get_rube_client()
    result = await client.search_tools("send an email to john@example.com", "email:john@example.com")
    
    print(f"Search result: {result}")
    
    # Test workflow execution
    print("\n⚡ Testing workflow execution...")
    workflow_result = await client.execute_workflow([
        {"tool_slug": "GMAIL_SEND_EMAIL", "arguments": {"to": "test@example.com"}}
    ])
    
    print(f"Workflow result: {workflow_result}")
    
    # Test connection management
    print("\n🔗 Testing connection management...")
    connection_result = await client.manage_connections(["gmail", "slack"])
    
    print(f"Connection result: {connection_result}")
    
    print("\n🎉 RUBE integration test completed successfully!")
    return True

if __name__ == "__main__":
    asyncio.run(test_rube_integration())
