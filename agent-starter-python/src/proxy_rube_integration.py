"""
Proxy-based RUBE MCP Integration for LiveKit Agent
This module connects to a RUBE MCP proxy server for real app automation.
"""

import os
import logging
import asyncio
from typing import Dict, Any, Optional, List
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.local")

logger = logging.getLogger("proxy_rube_integration")

class ProxyRubeMCPClient:
    """Client that connects to RUBE MCP proxy server for real functionality"""
    
    def __init__(self, proxy_url: str = "http://localhost:8001"):
        self.proxy_url = proxy_url
        self.api_key = os.getenv("RUBE_API_KEY")
        self.initialized = False
        
    async def initialize(self):
        """Initialize connection to RUBE MCP proxy"""
        if not self.api_key:
            logger.error("RUBE_API_KEY not found in environment variables")
            return False
            
        try:
            # Test connection to proxy server
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.proxy_url}/health")
                if response.status_code == 200:
                    logger.info("Successfully connected to RUBE MCP proxy server")
                    self.initialized = True
                    return True
                else:
                    logger.error(f"Proxy server health check failed: {response.status_code}")
                    return False
        except Exception as e:
            logger.error(f"Failed to connect to RUBE MCP proxy: {e}")
            return False
    
    async def search_tools(self, use_case: str, known_fields: str = "") -> Dict[str, Any]:
        """Search for tools using the RUBE MCP proxy"""
        if not self.initialized:
            return {"success": False, "error": "Proxy client not initialized"}
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.proxy_url}/search-tools",
                    json={
                        "use_case": use_case,
                        "known_fields": known_fields,
                        "session": {"generate_id": True}
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("data", {})
                else:
                    logger.error(f"Search tools failed: {response.status_code} - {response.text}")
                    return {"success": False, "error": f"HTTP {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error searching tools via proxy: {e}")
            return {"success": False, "error": str(e)}
    
    async def execute_workflow(self, tools: List[Dict[str, Any]], session_id: str = None) -> Dict[str, Any]:
        """Execute workflow using the RUBE MCP proxy"""
        if not self.initialized:
            return {"success": False, "error": "Proxy client not initialized"}
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.proxy_url}/execute-workflow",
                    json={
                        "tools": tools,
                        "memory": {},
                        "session_id": session_id or "workflow-session",
                        "sync_response_to_workbench": False,
                        "thought": f"Executing workflow with {len(tools)} tools",
                        "current_step": "EXECUTING_WORKFLOW",
                        "current_step_metric": {
                            "completed": 0,
                            "total": len(tools),
                            "unit": "tools"
                        },
                        "next_step": "WORKFLOW_COMPLETE"
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("data", {})
                else:
                    logger.error(f"Execute workflow failed: {response.status_code} - {response.text}")
                    return {"success": False, "error": f"HTTP {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error executing workflow via proxy: {e}")
            return {"success": False, "error": str(e)}
    
    async def manage_connections(self, toolkits: List[str]) -> Dict[str, Any]:
        """Manage connections using the RUBE MCP proxy"""
        if not self.initialized:
            return {"success": False, "error": "Proxy client not initialized"}
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.proxy_url}/manage-connections",
                    json={
                        "toolkits": toolkits,
                        "specify_custom_auth": {}
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("data", {})
                else:
                    logger.error(f"Manage connections failed: {response.status_code} - {response.text}")
                    return {"success": False, "error": f"HTTP {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error managing connections via proxy: {e}")
            return {"success": False, "error": str(e)}
    
    async def create_plan(self, use_case: str, difficulty: str = "medium") -> Dict[str, Any]:
        """Create workflow plan using the RUBE MCP proxy"""
        if not self.initialized:
            return {"success": False, "error": "Proxy client not initialized"}
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.proxy_url}/create-plan",
                    json={
                        "use_case": use_case,
                        "difficulty": difficulty,
                        "known_fields": "",
                        "primary_tool_slugs": [],
                        "reasoning": f"Creating plan for: {use_case}",
                        "session_id": "plan-session"
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("data", {})
                else:
                    logger.error(f"Create plan failed: {response.status_code} - {response.text}")
                    return {"success": False, "error": f"HTTP {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Error creating plan via proxy: {e}")
            return {"success": False, "error": str(e)}

# Global proxy client instance
proxy_rube_client = ProxyRubeMCPClient()

async def initialize_proxy_rube():
    """Initialize the proxy RUBE client"""
    return await proxy_rube_client.initialize()

def get_proxy_rube_client() -> ProxyRubeMCPClient:
    """Get the proxy RUBE client instance"""
    return proxy_rube_client
