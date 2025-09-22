#!/usr/bin/env python3
"""
Voice Automation Demo - Demonstrate the complete working system
"""

import asyncio
import httpx
import json

async def demo_email_automation():
    """Demo: Email automation workflow"""
    print("📧 DEMO: Email Automation")
    print("-" * 30)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient() as client:
        print("👤 User says: 'Send an email to sarah@company.com about tomorrow's meeting'")
        print()
        
        # Agent searches for tools
        print("🔍 Agent: Let me search for email tools...")
        search_response = await client.post(f"{base_url}/search-tools", json={
            "use_case": "send an email to sarah@company.com about tomorrow's meeting",
            "known_fields": "email:sarah@company.com"
        })
        
        if search_response.status_code == 200:
            result = search_response.json()
            tools = result['data']['tools']
            session_id = result['data']['session_id']
            print(f"✅ Found {len(tools)} email tools: {', '.join(tools[:3])}")
            print(f"📋 Session: {session_id}")
        else:
            print("❌ Search failed")
            return False
        
        print()
        
        # Agent executes workflow
        print("⚡ Agent: Executing email workflow...")
        execute_response = await client.post(f"{base_url}/execute-workflow", json={
            "tools": [{"tool_slug": "GMAIL_SEND_EMAIL", "arguments": {
                "to": "sarah@company.com",
                "subject": "Tomorrow's Meeting",
                "body": "Hi Sarah, confirming our meeting tomorrow at 2 PM."
            }}],
            "session_id": session_id
        })
        
        if execute_response.status_code == 200:
            result = execute_response.json()
            print(f"✅ {result['data']['message']}")
            print("🤖 Agent: 'I've sent the email to Sarah about tomorrow's meeting!'")
        else:
            print("❌ Execution failed")
            return False
        
        return True

async def demo_document_creation():
    """Demo: Document creation workflow"""
    print("\n📄 DEMO: Document Creation")
    print("-" * 30)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient() as client:
        print("👤 User says: 'Create a Google Doc called Project Plan'")
        print()
        
        print("🔍 Agent: Searching for document tools...")
        search_response = await client.post(f"{base_url}/search-tools", json={
            "use_case": "create a Google Doc called Project Plan"
        })
        
        if search_response.status_code == 200:
            result = search_response.json()
            tools = result['data']['tools']
            print(f"✅ Found document tools: {', '.join(tools)}")
        else:
            print("❌ Search failed")
            return False
        
        print()
        print("📝 Agent: Creating document...")
        execute_response = await client.post(f"{base_url}/execute-workflow", json={
            "tools": [{"tool_slug": "GOOGLE_DOCS_CREATE", "arguments": {
                "title": "Project Plan",
                "content": "# Project Plan\n\nCreated by voice command"
            }}]
        })
        
        if execute_response.status_code == 200:
            print("✅ Document created successfully")
            print("🤖 Agent: 'I've created the Project Plan document in Google Docs!'")
        else:
            print("❌ Creation failed")
            return False
        
        return True

async def demo_app_connections():
    """Demo: App connection management"""
    print("\n🔗 DEMO: App Connections")
    print("-" * 30)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient() as client:
        print("👤 User says: 'Connect to Gmail and Slack'")
        print()
        
        print("🔗 Agent: Setting up app connections...")
        response = await client.post(f"{base_url}/manage-connections", json={
            "toolkits": ["gmail", "slack"]
        })
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['data']['message']}")
            print("🤖 Agent: 'I've initiated connections to Gmail and Slack. You may need to authenticate.'")
        else:
            print("❌ Connection setup failed")
            return False
        
        return True

def show_system_status():
    """Show current system status"""
    print("🌟 LIVEKIT VOICE AI SYSTEM STATUS")
    print("=" * 50)
    
    # Check services
    try:
        import requests
        
        # Check proxy server
        try:
            response = requests.get("http://localhost:8001/health", timeout=2)
            if response.status_code == 200:
                print("✅ RUBE Proxy Server: RUNNING (port 8001)")
            else:
                print("❌ RUBE Proxy Server: ERROR")
        except:
            print("❌ RUBE Proxy Server: NOT RUNNING")
        
        # Check frontend
        try:
            response = requests.get("http://localhost:3001", timeout=2)
            if response.status_code == 200:
                print("✅ React Frontend: RUNNING (port 3001)")
            else:
                print("❌ React Frontend: ERROR")
        except:
            print("❌ React Frontend: NOT RUNNING")
        
        print("🤖 LiveKit Agent: Check terminal for status")
        
    except ImportError:
        print("📊 Service status check requires 'requests' module")

async def run_complete_demo():
    """Run the complete voice automation demo"""
    show_system_status()
    print()
    
    print("🎤 VOICE AUTOMATION DEMOS")
    print("=" * 50)
    
    # Demo 1: Email automation
    success1 = await demo_email_automation()
    
    # Demo 2: Document creation
    success2 = await demo_document_creation()
    
    # Demo 3: App connections
    success3 = await demo_app_connections()
    
    print("\n🎯 DEMO RESULTS")
    print("=" * 50)
    print(f"📧 Email Automation: {'✅ SUCCESS' if success1 else '❌ FAILED'}")
    print(f"📄 Document Creation: {'✅ SUCCESS' if success2 else '❌ FAILED'}")
    print(f"🔗 App Connections: {'✅ SUCCESS' if success3 else '❌ FAILED'}")
    
    if all([success1, success2, success3]):
        print("\n🎉 ALL DEMOS SUCCESSFUL!")
        print("\n🚀 READY FOR VOICE COMMANDS!")
        print("Open http://localhost:3001 and try:")
        print("  • 'What apps can you integrate with?'")
        print("  • 'Send an email to john@example.com'")
        print("  • 'Create a document called Meeting Notes'")
        print("  • 'Connect to Gmail and Slack'")
        print("  • 'Post to LinkedIn about our product'")
    else:
        print("\n⚠️  Some demos failed - check service status")

if __name__ == "__main__":
    asyncio.run(run_complete_demo())
