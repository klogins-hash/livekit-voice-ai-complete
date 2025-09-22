#!/usr/bin/env python3
"""
Complete Integration Test Script
Tests the entire LiveKit Voice AI system with RUBE MCP integration.
"""

import asyncio
import httpx
import json
import sys
from pathlib import Path

async def test_proxy_server():
    """Test the RUBE proxy server"""
    print("🔍 Testing RUBE Proxy Server")
    print("-" * 30)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient() as client:
        # Test health endpoint
        try:
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                print("✅ Proxy server health check passed")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to proxy server: {e}")
            print("   Make sure to start: python3 rube_proxy_server.py")
            return False
        
        # Test tool search
        try:
            search_data = {
                "use_case": "send an email to sarah@company.com about the meeting",
                "known_fields": "email:sarah@company.com"
            }
            response = await client.post(f"{base_url}/search-tools", json=search_data)
            if response.status_code == 200:
                result = response.json()
                print("✅ Tool search test passed")
                print(f"   Found tools: {result['data']['tools']}")
                print(f"   Session ID: {result['data']['session_id']}")
                return result['data']['session_id']
            else:
                print(f"❌ Tool search failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Tool search error: {e}")
            return False

async def test_workflow_execution(session_id):
    """Test workflow execution"""
    print("\n⚡ Testing Workflow Execution")
    print("-" * 30)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient() as client:
        try:
            workflow_data = {
                "tools": [
                    {
                        "tool_slug": "GMAIL_SEND_EMAIL",
                        "arguments": {
                            "to": "sarah@company.com",
                            "subject": "Meeting Tomorrow",
                            "body": "Hi Sarah, just confirming our meeting tomorrow at 2 PM."
                        }
                    }
                ],
                "session_id": session_id,
                "thought": "Testing email workflow execution"
            }
            
            response = await client.post(f"{base_url}/execute-workflow", json=workflow_data)
            if response.status_code == 200:
                result = response.json()
                print("✅ Workflow execution test passed")
                print(f"   Results: {result['data']['message']}")
                print(f"   Status: {result['data']['results'][0]['status']}")
                return True
            else:
                print(f"❌ Workflow execution failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Workflow execution error: {e}")
            return False

async def test_connection_management():
    """Test app connection management"""
    print("\n🔗 Testing Connection Management")
    print("-" * 30)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient() as client:
        try:
            connection_data = {
                "toolkits": ["gmail", "slack", "google_docs"]
            }
            
            response = await client.post(f"{base_url}/manage-connections", json=connection_data)
            if response.status_code == 200:
                result = response.json()
                print("✅ Connection management test passed")
                print(f"   Apps: {', '.join(connection_data['toolkits'])}")
                return True
            else:
                print(f"❌ Connection management failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection management error: {e}")
            return False

async def test_agent_proxy_connection():
    """Test agent connection to proxy"""
    print("\n🤖 Testing Agent-Proxy Connection")
    print("-" * 30)
    
    sys.path.insert(0, str(Path("agent-starter-python/src")))
    
    try:
        from proxy_rube_integration import ProxyRubeMCPClient
        
        client = ProxyRubeMCPClient()
        success = await client.initialize()
        
        if success:
            print("✅ Agent can connect to proxy server")
            
            # Test tool search through agent client
            result = await client.search_tools("create a Google Doc called Test Document")
            if result:
                print("✅ Agent can search tools through proxy")
                print(f"   Found: {result.get('tools', [])}")
                return True
            else:
                print("❌ Agent tool search failed")
                return False
        else:
            print("❌ Agent cannot connect to proxy server")
            return False
            
    except Exception as e:
        print(f"❌ Agent-proxy connection error: {e}")
        return False

def check_services_status():
    """Check status of all services"""
    print("📊 Service Status Check")
    print("-" * 30)
    
    # Check proxy server
    try:
        import requests
        response = requests.get("http://localhost:8001/health", timeout=2)
        if response.status_code == 200:
            print("✅ RUBE Proxy Server: Running on port 8001")
        else:
            print("❌ RUBE Proxy Server: Not responding")
    except:
        print("❌ RUBE Proxy Server: Not running")
    
    # Check frontend
    try:
        response = requests.get("http://localhost:3001", timeout=2)
        if response.status_code == 200:
            print("✅ React Frontend: Running on port 3001")
        else:
            print("❌ React Frontend: Not responding")
    except:
        print("❌ React Frontend: Not running")
    
    # Check agent (this is harder to test directly)
    print("🤖 LiveKit Agent: Check logs above for connection status")

async def run_complete_test():
    """Run the complete integration test"""
    print("🧪 Complete LiveKit Voice AI Integration Test")
    print("=" * 50)
    
    # Test proxy server
    session_id = await test_proxy_server()
    if not session_id:
        print("\n❌ Proxy server tests failed")
        return False
    
    # Test workflow execution
    workflow_success = await test_workflow_execution(session_id)
    if not workflow_success:
        print("\n❌ Workflow execution tests failed")
        return False
    
    # Test connection management
    connection_success = await test_connection_management()
    if not connection_success:
        print("\n❌ Connection management tests failed")
        return False
    
    # Test agent-proxy connection
    agent_success = await test_agent_proxy_connection()
    if not agent_success:
        print("\n❌ Agent-proxy connection tests failed")
        return False
    
    print("\n🎉 All Integration Tests Passed!")
    print("=" * 50)
    print("✅ RUBE Proxy Server: Operational")
    print("✅ Tool Discovery: Working")
    print("✅ Workflow Execution: Working")
    print("✅ Connection Management: Working")
    print("✅ Agent Integration: Working")
    
    print("\n🚀 Next Steps:")
    print("1. Open http://localhost:3001 in your browser")
    print("2. Click 'Start call' and grant microphone permissions")
    print("3. Try voice commands like:")
    print("   • 'What apps can you integrate with?'")
    print("   • 'Send an email to john@example.com'")
    print("   • 'Create a Google Doc called Meeting Notes'")
    print("   • 'Connect to Gmail and Slack'")
    
    return True

if __name__ == "__main__":
    # Check service status first
    check_services_status()
    print()
    
    # Run async tests
    success = asyncio.run(run_complete_test())
    sys.exit(0 if success else 1)
