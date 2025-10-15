#!/usr/bin/env python3
"""
Real MCP Integration Test - Test actual RUBE MCP tools
This will attempt to call the real RUBE MCP functions directly.
"""

import asyncio
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("real_mcp_test")

async def test_real_rube_search_tools():
    """Test the actual RUBE_SEARCH_TOOLS function"""
    print("🔍 Testing Real RUBE_SEARCH_TOOLS")
    print("-" * 40)
    
    try:
        # Test 1: Email tools search
        print("Test 1: Searching for email tools...")
        result = await mcp0_rube__RUBE_SEARCH_TOOLS({
            "use_case": "send an email to test@example.com with subject 'Test Email'",
            "known_fields": "email:test@example.com,subject:Test Email",
            "session": {"generate_id": True}
        })
        
        print(f"✅ Email search result: {json.dumps(result, indent=2)}")
        
        # Test 2: Document tools search
        print("\nTest 2: Searching for document tools...")
        result2 = await mcp0_rube__RUBE_SEARCH_TOOLS({
            "use_case": "create a Google Doc called 'Test Document'",
            "known_fields": "document_name:Test Document",
            "session": {"generate_id": True}
        })
        
        print(f"✅ Document search result: {json.dumps(result2, indent=2)}")
        
        # Test 3: Social media tools search
        print("\nTest 3: Searching for social media tools...")
        result3 = await mcp0_rube__RUBE_SEARCH_TOOLS({
            "use_case": "post to LinkedIn about our company update",
            "known_fields": "platform:linkedin",
            "session": {"generate_id": True}
        })
        
        print(f"✅ Social media search result: {json.dumps(result3, indent=2)}")
        
        return True
        
    except NameError as e:
        print(f"❌ RUBE MCP tools not available in this context: {e}")
        print("This is expected if running outside MCP environment")
        return False
    except Exception as e:
        print(f"❌ Error testing RUBE search tools: {e}")
        return False

async def test_real_rube_execute_tool():
    """Test the actual RUBE_MULTI_EXECUTE_TOOL function"""
    print("\n⚡ Testing Real RUBE_MULTI_EXECUTE_TOOL")
    print("-" * 40)
    
    try:
        # Test 1: Execute a simple email workflow
        print("Test 1: Executing email workflow...")
        result = await mcp0_rube__RUBE_MULTI_EXECUTE_TOOL({
            "tools": [
                {
                    "tool_slug": "GMAIL_SEND_EMAIL",
                    "arguments": {
                        "to": "test@example.com",
                        "subject": "MCP Integration Test",
                        "body": "This is a test email from the MCP integration system."
                    }
                }
            ],
            "memory": {},
            "session_id": "test-session-001",
            "sync_response_to_workbench": False,
            "thought": "Testing real email sending through MCP",
            "current_step": "SENDING_EMAIL",
            "current_step_metric": {
                "completed": 0,
                "total": 1,
                "unit": "emails"
            },
            "next_step": "EMAIL_SENT"
        })
        
        print(f"✅ Email execution result: {json.dumps(result, indent=2)}")
        
        # Test 2: Execute document creation
        print("\nTest 2: Executing document creation...")
        result2 = await mcp0_rube__RUBE_MULTI_EXECUTE_TOOL({
            "tools": [
                {
                    "tool_slug": "GOOGLE_DOCS_CREATE",
                    "arguments": {
                        "title": "MCP Test Document",
                        "content": "# MCP Integration Test\n\nThis document was created via MCP integration."
                    }
                }
            ],
            "memory": {},
            "session_id": "test-session-002",
            "sync_response_to_workbench": False,
            "thought": "Testing real document creation through MCP"
        })
        
        print(f"✅ Document creation result: {json.dumps(result2, indent=2)}")
        
        return True
        
    except NameError as e:
        print(f"❌ RUBE MCP tools not available in this context: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing RUBE execute tool: {e}")
        return False

async def test_real_rube_manage_connections():
    """Test the actual RUBE_MANAGE_CONNECTIONS function"""
    print("\n🔗 Testing Real RUBE_MANAGE_CONNECTIONS")
    print("-" * 40)
    
    try:
        # Test connection management
        print("Testing connection management...")
        result = await mcp0_rube__RUBE_MANAGE_CONNECTIONS({
            "toolkits": ["gmail", "google_docs", "linkedin"],
            "specify_custom_auth": {}
        })
        
        print(f"✅ Connection management result: {json.dumps(result, indent=2)}")
        return True
        
    except NameError as e:
        print(f"❌ RUBE MCP tools not available in this context: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing RUBE manage connections: {e}")
        return False

async def test_real_rube_create_plan():
    """Test the actual RUBE_CREATE_PLAN function"""
    print("\n📋 Testing Real RUBE_CREATE_PLAN")
    print("-" * 40)
    
    try:
        # Test plan creation
        print("Testing workflow plan creation...")
        result = await mcp0_rube__RUBE_CREATE_PLAN({
            "use_case": "send a follow-up email and create a meeting agenda",
            "difficulty": "medium",
            "known_fields": "email:followup@example.com,meeting_type:weekly_standup",
            "primary_tool_slugs": ["GMAIL_SEND_EMAIL", "GOOGLE_DOCS_CREATE"],
            "reasoning": "Creating a plan for email follow-up and meeting preparation",
            "session_id": "plan-test-session"
        })
        
        print(f"✅ Plan creation result: {json.dumps(result, indent=2)}")
        return True
        
    except NameError as e:
        print(f"❌ RUBE MCP tools not available in this context: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing RUBE create plan: {e}")
        return False

async def test_available_mcp_tools():
    """Test what MCP tools are actually available"""
    print("\n🔧 Testing Available MCP Tools")
    print("-" * 40)
    
    # Check what's available in the global namespace
    available_tools = []
    
    # Common RUBE MCP tool patterns
    potential_tools = [
        'mcp0_rube__RUBE_SEARCH_TOOLS',
        'mcp0_rube__RUBE_MULTI_EXECUTE_TOOL', 
        'mcp0_rube__RUBE_MANAGE_CONNECTIONS',
        'mcp0_rube__RUBE_CREATE_PLAN',
        'RUBE_SEARCH_TOOLS',
        'RUBE_MULTI_EXECUTE_TOOL',
        'RUBE_MANAGE_CONNECTIONS',
        'RUBE_CREATE_PLAN'
    ]
    
    for tool in potential_tools:
        try:
            if tool in globals():
                available_tools.append(tool)
                print(f"✅ Found: {tool}")
            else:
                print(f"❌ Not found: {tool}")
        except:
            print(f"❌ Error checking: {tool}")
    
    print(f"\n📊 Available MCP tools: {len(available_tools)}")
    return available_tools

async def run_comprehensive_mcp_test():
    """Run comprehensive MCP integration tests"""
    print("🧪 COMPREHENSIVE REAL MCP INTEGRATION TEST")
    print("=" * 60)
    
    # Test 1: Check available tools
    available_tools = await test_available_mcp_tools()
    
    # Test 2: Search tools
    search_success = await test_real_rube_search_tools()
    
    # Test 3: Execute workflows
    execute_success = await test_real_rube_execute_tool()
    
    # Test 4: Manage connections
    connection_success = await test_real_rube_manage_connections()
    
    # Test 5: Create plans
    plan_success = await test_real_rube_create_plan()
    
    print("\n🎯 REAL MCP TEST RESULTS")
    print("=" * 60)
    print(f"Available Tools: {len(available_tools)} found")
    print(f"Search Tools: {'✅ SUCCESS' if search_success else '❌ FAILED'}")
    print(f"Execute Workflows: {'✅ SUCCESS' if execute_success else '❌ FAILED'}")
    print(f"Manage Connections: {'✅ SUCCESS' if connection_success else '❌ FAILED'}")
    print(f"Create Plans: {'✅ SUCCESS' if plan_success else '❌ FAILED'}")
    
    if any([search_success, execute_success, connection_success, plan_success]):
        print("\n🎉 REAL MCP INTEGRATION WORKING!")
        print("Some or all RUBE MCP tools are functional")
    else:
        print("\n⚠️  MCP TOOLS NOT AVAILABLE IN THIS CONTEXT")
        print("This is expected when running outside the MCP environment")
        print("The proxy server approach is the correct solution")
    
    return {
        'available_tools': available_tools,
        'search_success': search_success,
        'execute_success': execute_success,
        'connection_success': connection_success,
        'plan_success': plan_success
    }

if __name__ == "__main__":
    result = asyncio.run(run_comprehensive_mcp_test())
