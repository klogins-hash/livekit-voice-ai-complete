#!/usr/bin/env python3
"""
Advanced Voice Automation Workflows
Demonstrates complex multi-step automation scenarios.
"""

import asyncio
import httpx
import json

async def workflow_social_media_campaign():
    """Advanced: Social media campaign workflow"""
    print("📱 ADVANCED: Social Media Campaign")
    print("-" * 40)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient() as client:
        print("👤 User: 'Create a social media campaign about our new product launch'")
        print()
        
        # Step 1: Search for social media tools
        print("🔍 Step 1: Finding social media tools...")
        search_response = await client.post(f"{base_url}/search-tools", json={
            "use_case": "create social media posts for product launch campaign"
        })
        
        if search_response.status_code == 200:
            result = search_response.json()
            tools = result['data']['tools']
            session_id = result['data']['session_id']
            print(f"✅ Found tools: {', '.join(tools)}")
        else:
            print("❌ Tool search failed")
            return False
        
        # Step 2: Execute multi-platform posting
        print("\n📝 Step 2: Creating posts for multiple platforms...")
        platforms = [
            {"tool": "LINKEDIN_POST", "message": "Excited to announce our new product! 🚀 #innovation #tech"},
            {"tool": "TWITTER_POST", "message": "🎉 New product launch! Check it out: link.com/product"},
            {"tool": "FACEBOOK_POST", "message": "We're thrilled to share our latest innovation with you!"}
        ]
        
        for platform in platforms:
            execute_response = await client.post(f"{base_url}/execute-workflow", json={
                "tools": [{"tool_slug": platform["tool"], "arguments": {"content": platform["message"]}}],
                "session_id": session_id
            })
            
            if execute_response.status_code == 200:
                print(f"✅ Posted to {platform['tool'].replace('_POST', '')}")
            else:
                print(f"❌ Failed to post to {platform['tool']}")
        
        print("\n🤖 Agent: 'I've created and posted your product launch campaign across LinkedIn, Twitter, and Facebook!'")
        return True

async def workflow_meeting_automation():
    """Advanced: Complete meeting automation"""
    print("\n📅 ADVANCED: Meeting Automation")
    print("-" * 40)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient() as client:
        print("👤 User: 'Schedule a team meeting for tomorrow at 2 PM and send invites'")
        print()
        
        # Step 1: Create calendar event
        print("📅 Step 1: Creating calendar event...")
        calendar_response = await client.post(f"{base_url}/execute-workflow", json={
            "tools": [{
                "tool_slug": "GOOGLE_CALENDAR_CREATE_EVENT",
                "arguments": {
                    "title": "Team Meeting",
                    "date": "2025-09-23",
                    "time": "14:00",
                    "duration": "60 minutes",
                    "attendees": ["sarah@company.com", "john@company.com", "mike@company.com"]
                }
            }]
        })
        
        if calendar_response.status_code == 200:
            print("✅ Calendar event created")
        else:
            print("❌ Calendar creation failed")
            return False
        
        # Step 2: Send email invitations
        print("\n📧 Step 2: Sending email invitations...")
        attendees = ["sarah@company.com", "john@company.com", "mike@company.com"]
        
        for attendee in attendees:
            email_response = await client.post(f"{base_url}/execute-workflow", json={
                "tools": [{
                    "tool_slug": "GMAIL_SEND_EMAIL",
                    "arguments": {
                        "to": attendee,
                        "subject": "Team Meeting Tomorrow - 2 PM",
                        "body": "Hi! You're invited to our team meeting tomorrow at 2 PM. Calendar invite attached."
                    }
                }]
            })
            
            if email_response.status_code == 200:
                print(f"✅ Invitation sent to {attendee}")
            else:
                print(f"❌ Failed to send to {attendee}")
        
        # Step 3: Create meeting agenda document
        print("\n📄 Step 3: Creating meeting agenda...")
        doc_response = await client.post(f"{base_url}/execute-workflow", json={
            "tools": [{
                "tool_slug": "GOOGLE_DOCS_CREATE",
                "arguments": {
                    "title": "Team Meeting Agenda - Sept 23",
                    "content": "# Team Meeting Agenda\n\n1. Project Updates\n2. Q4 Planning\n3. Action Items\n4. Next Steps"
                }
            }]
        })
        
        if doc_response.status_code == 200:
            print("✅ Meeting agenda created")
        else:
            print("❌ Agenda creation failed")
        
        print("\n🤖 Agent: 'I've scheduled the team meeting, sent invitations to all attendees, and created the agenda document!'")
        return True

async def workflow_project_kickoff():
    """Advanced: Project kickoff automation"""
    print("\n🚀 ADVANCED: Project Kickoff")
    print("-" * 40)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient() as client:
        print("👤 User: 'Start a new project called Mobile App and set up everything'")
        print()
        
        # Step 1: Create project repository
        print("📁 Step 1: Creating GitHub repository...")
        repo_response = await client.post(f"{base_url}/execute-workflow", json={
            "tools": [{
                "tool_slug": "GITHUB_CREATE_REPO",
                "arguments": {
                    "name": "mobile-app-project",
                    "description": "New mobile app development project",
                    "private": False
                }
            }]
        })
        
        if repo_response.status_code == 200:
            print("✅ GitHub repository created")
        else:
            print("❌ Repository creation failed")
        
        # Step 2: Create project documentation
        print("\n📚 Step 2: Creating project documentation...")
        docs = [
            {"title": "Project Overview", "content": "# Mobile App Project\n\nProject goals and objectives"},
            {"title": "Technical Specifications", "content": "# Technical Specs\n\nArchitecture and requirements"},
            {"title": "Development Timeline", "content": "# Timeline\n\nMilestones and deadlines"}
        ]
        
        for doc in docs:
            doc_response = await client.post(f"{base_url}/execute-workflow", json={
                "tools": [{
                    "tool_slug": "GOOGLE_DOCS_CREATE",
                    "arguments": {
                        "title": doc["title"],
                        "content": doc["content"]
                    }
                }]
            })
            
            if doc_response.status_code == 200:
                print(f"✅ Created: {doc['title']}")
            else:
                print(f"❌ Failed: {doc['title']}")
        
        # Step 3: Set up project tracking
        print("\n📊 Step 3: Setting up project tracking...")
        jira_response = await client.post(f"{base_url}/execute-workflow", json={
            "tools": [{
                "tool_slug": "JIRA_CREATE_PROJECT",
                "arguments": {
                    "name": "Mobile App Development",
                    "key": "MAD",
                    "type": "software"
                }
            }]
        })
        
        if jira_response.status_code == 200:
            print("✅ Jira project created")
        else:
            print("❌ Jira setup failed")
        
        # Step 4: Notify team
        print("\n📢 Step 4: Notifying team...")
        slack_response = await client.post(f"{base_url}/execute-workflow", json={
            "tools": [{
                "tool_slug": "SLACK_SEND_MESSAGE",
                "arguments": {
                    "channel": "#development",
                    "message": "🚀 New project started: Mobile App Development! Check out the repo and docs."
                }
            }]
        })
        
        if slack_response.status_code == 200:
            print("✅ Team notified via Slack")
        else:
            print("❌ Slack notification failed")
        
        print("\n🤖 Agent: 'I've set up your Mobile App project with GitHub repo, documentation, Jira tracking, and notified the team!'")
        return True

async def workflow_customer_support():
    """Advanced: Customer support automation"""
    print("\n🎧 ADVANCED: Customer Support")
    print("-" * 40)
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient() as client:
        print("👤 User: 'Handle the customer complaint about billing and follow up'")
        print()
        
        # Step 1: Create support ticket
        print("🎫 Step 1: Creating support ticket...")
        ticket_response = await client.post(f"{base_url}/execute-workflow", json={
            "tools": [{
                "tool_slug": "JIRA_CREATE_ISSUE",
                "arguments": {
                    "project": "SUPPORT",
                    "type": "Bug",
                    "summary": "Customer billing complaint",
                    "description": "Customer reported billing discrepancy - needs investigation",
                    "priority": "High"
                }
            }]
        })
        
        if ticket_response.status_code == 200:
            print("✅ Support ticket created")
        else:
            print("❌ Ticket creation failed")
        
        # Step 2: Send acknowledgment email
        print("\n📧 Step 2: Sending acknowledgment email...")
        email_response = await client.post(f"{base_url}/execute-workflow", json={
            "tools": [{
                "tool_slug": "GMAIL_SEND_EMAIL",
                "arguments": {
                    "to": "customer@example.com",
                    "subject": "Re: Billing Inquiry - We're Looking Into It",
                    "body": "Thank you for contacting us about your billing concern. We've created ticket #12345 and our team is investigating. We'll follow up within 24 hours."
                }
            }]
        })
        
        if email_response.status_code == 200:
            print("✅ Acknowledgment email sent")
        else:
            print("❌ Email failed")
        
        # Step 3: Notify support team
        print("\n👥 Step 3: Notifying support team...")
        slack_response = await client.post(f"{base_url}/execute-workflow", json={
            "tools": [{
                "tool_slug": "SLACK_SEND_MESSAGE",
                "arguments": {
                    "channel": "#support",
                    "message": "🚨 High priority billing complaint - Ticket #12345 created. Customer: customer@example.com"
                }
            }]
        })
        
        if slack_response.status_code == 200:
            print("✅ Support team notified")
        else:
            print("❌ Slack notification failed")
        
        print("\n🤖 Agent: 'I've created a support ticket, sent an acknowledgment to the customer, and alerted the support team!'")
        return True

async def run_advanced_workflows():
    """Run all advanced workflow demonstrations"""
    print("🎯 ADVANCED VOICE AUTOMATION WORKFLOWS")
    print("=" * 60)
    
    workflows = [
        ("Social Media Campaign", workflow_social_media_campaign),
        ("Meeting Automation", workflow_meeting_automation),
        ("Project Kickoff", workflow_project_kickoff),
        ("Customer Support", workflow_customer_support)
    ]
    
    results = []
    
    for name, workflow_func in workflows:
        try:
            success = await workflow_func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            results.append((name, False))
    
    print("\n🏆 ADVANCED WORKFLOW RESULTS")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{name}: {status}")
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n📊 Overall Success Rate: {successful}/{total} ({successful/total*100:.0f}%)")
    
    if successful == total:
        print("\n🎉 ALL ADVANCED WORKFLOWS SUCCESSFUL!")
        print("\nYour voice AI can now handle complex multi-step automation:")
        print("  • Multi-platform social media campaigns")
        print("  • Complete meeting setup and coordination")
        print("  • Full project initialization and setup")
        print("  • End-to-end customer support workflows")
        print("\n🚀 Ready for enterprise-level voice automation!")
    else:
        print(f"\n⚠️  {total - successful} workflows need attention")

if __name__ == "__main__":
    asyncio.run(run_advanced_workflows())
