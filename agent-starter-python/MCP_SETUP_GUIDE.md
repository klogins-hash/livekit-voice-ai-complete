# 🔧 Real RUBE MCP Integration Setup Guide

## ❗ Current Status: Mock Integration

The current RUBE integration is a **demonstration/mock version**. To enable **real app automation** (actually sending emails, creating documents, etc.), you need to configure proper MCP tool access.

## 🎯 What's Needed for Real Integration

### 1. MCP Server Configuration

The agent needs to be configured to connect to the RUBE MCP server directly. This requires:

```python
# In the agent code, you need access to the actual MCP tools:
from mcp_tools import mcp0_rube__RUBE_SEARCH_TOOLS
from mcp_tools import mcp0_rube__RUBE_MULTI_EXECUTE_TOOL
from mcp_tools import mcp0_rube__RUBE_MANAGE_CONNECTIONS
```

### 2. MCP Client Setup

Configure the MCP client to connect to RUBE:

```python
import mcp
from mcp.client.stdio import stdio_client

# Configure MCP client for RUBE
async def setup_rube_mcp():
    server_params = mcp.StdioServerParameters(
        command="rube-mcp-server",
        args=["--api-key", os.getenv("RUBE_API_KEY")]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with mcp.ClientSession(read, write) as session:
            # Initialize RUBE MCP session
            await session.initialize()
            return session
```

### 3. Environment Configuration

Ensure proper environment setup:

```env
# .env.local
RUBE_API_KEY=Bearer eyJhbGciOiJIUzI1NiJ9...
RUBE_MCP_SERVER_URL=https://rube.app/mcp
RUBE_MCP_ENABLED=true
```

## 🚀 Implementation Options

### Option 1: Direct MCP Integration

Modify the agent to use MCP tools directly:

```python
@function_tool
async def search_rube_tools(self, context: RunContext, task_description: str):
    # Call actual RUBE MCP tool
    result = await mcp0_rube__RUBE_SEARCH_TOOLS({
        "use_case": task_description,
        "known_fields": "",
        "session": {"generate_id": True}
    })
    return result
```

### Option 2: MCP Proxy Service

Create a proxy service that bridges the agent to RUBE MCP:

```python
# mcp_proxy.py
class RubeMCPProxy:
    async def search_tools(self, use_case: str):
        # Forward to actual RUBE MCP server
        async with self.mcp_session as session:
            return await session.call_tool("RUBE_SEARCH_TOOLS", {
                "use_case": use_case
            })
```

### Option 3: HTTP API Integration

Use RUBE's HTTP API directly:

```python
import httpx

async def call_rube_api(endpoint: str, data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://rube.app/api/{endpoint}",
            headers={"Authorization": os.getenv("RUBE_API_KEY")},
            json=data
        )
        return response.json()
```

## 🔧 Current Implementation Status

### ✅ What's Working
- Agent has RUBE function tools defined
- Environment variables configured
- Mock responses for testing
- Voice interface ready

### ❌ What's Missing for Real Functionality
- Actual MCP server connection
- Real tool execution
- App authentication flows
- Error handling for API failures

## 🎯 Next Steps to Enable Real Integration

### Step 1: Configure MCP Connection
```bash
# Install MCP client dependencies
pip install mcp-client

# Configure MCP server connection
export RUBE_MCP_SERVER="stdio:rube-mcp-server"
export RUBE_MCP_ARGS="--api-key=$RUBE_API_KEY"
```

### Step 2: Update Agent Code
Replace mock functions with real MCP calls:

```python
# Replace this mock code:
return {"success": True, "message": "Mock response"}

# With real MCP calls:
result = await self.mcp_session.call_tool("RUBE_SEARCH_TOOLS", params)
return result
```

### Step 3: Test Real Integration
```bash
# Test with real RUBE MCP server
uv run python src/mcp_agent.py console
```

## 🔍 Debugging Real Integration

### Check MCP Connection
```python
async def test_mcp_connection():
    try:
        # Test RUBE MCP server connection
        result = await mcp_session.list_tools()
        print(f"Available tools: {result}")
    except Exception as e:
        print(f"MCP connection failed: {e}")
```

### Verify API Key
```bash
# Test RUBE API key
curl -H "Authorization: Bearer $RUBE_API_KEY" https://rube.app/api/health
```

### Monitor Logs
```bash
# Watch agent logs for MCP errors
tail -f agent.log | grep -i "mcp\|rube"
```

## 📚 Resources

- **RUBE MCP Documentation**: Contact RUBE support for MCP server setup
- **MCP Protocol**: https://modelcontextprotocol.io/
- **LiveKit Agents**: https://docs.livekit.io/agents/

## 🎯 Summary

To enable **real app automation**:

1. **Configure MCP Server**: Set up connection to RUBE MCP server
2. **Update Agent Code**: Replace mock functions with real MCP calls  
3. **Test Integration**: Verify real tool execution
4. **Handle Authentication**: Set up app connection flows

The current implementation provides the **foundation** - you just need to connect it to the real RUBE MCP server for actual functionality.
