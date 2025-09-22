#!/usr/bin/env python3
"""
RUBE MCP Proxy Server
This server provides HTTP endpoints that call the actual RUBE MCP tools.
The LiveKit agent can then make HTTP requests to this proxy to access RUBE functionality.
"""

import asyncio
import json
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rube_proxy")

app = FastAPI(title="RUBE MCP Proxy", description="HTTP proxy for RUBE MCP tools")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "RUBE MCP Proxy Server", "status": "running"}

@app.post("/search-tools")
async def search_tools(request: Dict[str, Any]):
    """Search for RUBE tools using RUBE_SEARCH_TOOLS"""
    logger.info(f"Searching tools for: {request.get('use_case', 'unknown')}")
    
    try:
        # Call the actual RUBE_SEARCH_TOOLS MCP function
        result = await mcp0_rube__RUBE_SEARCH_TOOLS({
            "use_case": request.get("use_case", ""),
            "known_fields": request.get("known_fields", ""),
            "session": request.get("session", {"generate_id": True})
        })
        
        logger.info(f"Search result: {result}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"Error in search-tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute-workflow")
async def execute_workflow(request: Dict[str, Any]):
    """Execute workflow using RUBE_MULTI_EXECUTE_TOOL"""
    logger.info(f"Executing workflow with {len(request.get('tools', []))} tools")
    
    try:
        # Call the actual RUBE_MULTI_EXECUTE_TOOL MCP function
        result = await mcp0_rube__RUBE_MULTI_EXECUTE_TOOL({
            "tools": request.get("tools", []),
            "memory": request.get("memory", {}),
            "session_id": request.get("session_id", ""),
            "sync_response_to_workbench": request.get("sync_response_to_workbench", False),
            "thought": request.get("thought", "Executing workflow via proxy"),
            "current_step": request.get("current_step", "EXECUTING"),
            "current_step_metric": request.get("current_step_metric", {
                "completed": 0,
                "total": len(request.get("tools", [])),
                "unit": "tools"
            }),
            "next_step": request.get("next_step", "COMPLETE")
        })
        
        logger.info(f"Execution result: {result}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"Error in execute-workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/manage-connections")
async def manage_connections(request: Dict[str, Any]):
    """Manage app connections using RUBE_MANAGE_CONNECTIONS"""
    logger.info(f"Managing connections for: {request.get('toolkits', [])}")
    
    try:
        # Call the actual RUBE_MANAGE_CONNECTIONS MCP function
        result = await mcp0_rube__RUBE_MANAGE_CONNECTIONS({
            "toolkits": request.get("toolkits", []),
            "specify_custom_auth": request.get("specify_custom_auth", {})
        })
        
        logger.info(f"Connection result: {result}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"Error in manage-connections: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-plan")
async def create_plan(request: Dict[str, Any]):
    """Create workflow plan using RUBE_CREATE_PLAN"""
    logger.info(f"Creating plan for: {request.get('use_case', 'unknown')}")
    
    try:
        # Call the actual RUBE_CREATE_PLAN MCP function
        result = await mcp0_rube__RUBE_CREATE_PLAN({
            "use_case": request.get("use_case", ""),
            "difficulty": request.get("difficulty", "medium"),
            "known_fields": request.get("known_fields", ""),
            "primary_tool_slugs": request.get("primary_tool_slugs", []),
            "reasoning": request.get("reasoning", "Creating plan via proxy"),
            "session_id": request.get("session_id", "plan-session")
        })
        
        logger.info(f"Plan result: {result}")
        return {"success": True, "data": result}
        
    except Exception as e:
        logger.error(f"Error in create-plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "RUBE MCP Proxy is running"}

if __name__ == "__main__":
    print("🚀 Starting RUBE MCP Proxy Server...")
    print("This server provides HTTP access to RUBE MCP tools")
    print("Available endpoints:")
    print("  POST /search-tools - Search for RUBE tools")
    print("  POST /execute-workflow - Execute RUBE workflows")
    print("  POST /manage-connections - Manage app connections")
    print("  POST /create-plan - Create workflow plans")
    print("  GET /health - Health check")
    print("\nServer will run on http://localhost:8001")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
