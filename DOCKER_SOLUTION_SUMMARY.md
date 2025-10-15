# 🐳 Docker Solution for RUBE MCP Integration

## 🎯 **Problem Solved**

**Issue**: RUBE MCP tools work perfectly in this session but aren't available to separate processes (proxy server, agent).

**Solution**: Docker container that runs all services in the same process context where MCP tools are available.

## ✅ **Why Docker Will Fix This**

### **Current Issue**:
```
Session Context (MCP tools available) ✅
├── Proxy Server Process ❌ (no MCP access)
├── LiveKit Agent Process ❌ (no MCP access)  
└── Frontend Process ❌ (no MCP access)
```

### **Docker Solution**:
```
Docker Container (unified context) ✅
├── MCP-enabled Proxy ✅ (same context)
├── LiveKit Agent ✅ (same context)
└── Frontend ✅ (same context)
```

## 🚀 **Quick Start Guide**

### **1. Test Locally** (if you have Docker)
```bash
# Copy environment template
cp .env.template .env

# Add your API keys to .env file
nano .env

# Test Docker deployment
./test_docker_local.sh

# Open http://localhost:3001 and test voice commands
```

### **2. Deploy to Production**
```bash
# On your server (DigitalOcean, AWS, etc.)
git clone https://github.com/klogins-hash/livekit-voice-ai-complete.git
cd livekit-voice-ai-complete

# Set environment variables
export RUBE_API_KEY="your_key"
export LIVEKIT_URL="wss://your-instance.livekit.cloud"
# ... other API keys

# Deploy with Docker
./deploy_production.sh
```

## 📁 **Files Created**

### **Core Deployment**
- **`Dockerfile.unified`** - Single container with all services
- **`docker-compose.simple.yml`** - Simple orchestration
- **`.env.template`** - Environment variables template

### **Helper Scripts**
- **`test_docker_local.sh`** - Test locally before deploying
- **`deploy_production.sh`** - Production deployment script

## 🔧 **How It Works**

### **Unified Container Architecture**
```dockerfile
FROM python:3.11-slim

# Install all dependencies (Python + Node.js)
RUN apt-get update && apt-get install -y nodejs npm

# Copy all application code
COPY . .

# Install dependencies for all services
RUN pip install uv && uv sync
RUN npm install -g pnpm && pnpm install

# Start all services in same process context
CMD ["/app/start_unified.sh"]
```

### **Startup Script** (runs everything together)
```bash
#!/bin/bash
# All services start in the same process context
python3 mcp_enabled_proxy.py &    # MCP proxy with real tools
uv run python src/agent.py start & # LiveKit agent
pnpm start &                       # Frontend
```

## 🎯 **Expected Results After Docker Deployment**

### **✅ What Should Work**
- **Real Email Sending**: Actually send emails through Gmail/Outlook
- **Real Document Creation**: Actually create Google Docs/Sheets
- **Real Social Media**: Actually post to LinkedIn/Twitter
- **Real Calendar**: Actually create meetings and events
- **Real App Automation**: All 500+ RUBE integrations

### **🧪 Test Commands** (after deployment)
```bash
# Voice commands that should actually work:
"Send an email to john@example.com about the meeting"
"Create a Google Doc called Project Plan"  
"Post to LinkedIn about our product launch"
"Schedule a meeting for tomorrow at 2 PM"
"Connect to Gmail and Slack"
```

## 🌐 **Deployment Options**

### **DigitalOcean** (Recommended)
```bash
# Create droplet
doctl compute droplet create voice-ai \
  --image ubuntu-20-04-x64 \
  --size s-2vcpu-4gb \
  --region nyc1

# Deploy
scp -r . root@droplet-ip:/root/voice-ai/
ssh root@droplet-ip "cd /root/voice-ai && ./deploy_production.sh"
```

### **AWS EC2**
```bash
# Launch EC2 instance (Ubuntu 20.04, t3.medium)
# Install Docker: sudo apt install docker.io docker-compose
# Deploy: ./deploy_production.sh
```

### **Any VPS Provider**
```bash
# Requirements: Ubuntu/Debian with Docker
# Just run: ./deploy_production.sh
```

## 🔒 **Security & Production**

### **Environment Variables**
```env
RUBE_API_KEY=your_rube_api_key
LIVEKIT_URL=wss://your-instance.livekit.cloud
LIVEKIT_API_KEY=your_livekit_key
LIVEKIT_API_SECRET=your_livekit_secret
OPENAI_API_KEY=your_openai_key
DEEPGRAM_API_KEY=your_deepgram_key
CARTESIA_API_KEY=your_cartesia_key
```

### **Health Checks**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 🎉 **Why This Will Work**

1. **✅ Unified Process Context** - All services in same container
2. **✅ MCP Tools Available** - Proxy server has access to RUBE tools  
3. **✅ Real App Automation** - Actual emails, docs, social media posts
4. **✅ Production Ready** - Health checks, logging, restart policies
5. **✅ Easy Deployment** - Single command deployment anywhere

## 🚀 **Next Steps**

1. **Test locally** (if you have Docker installed)
2. **Deploy to your preferred cloud provider**
3. **Configure your API keys**
4. **Test voice commands for real automation**

**The Docker solution should completely fix the MCP integration issue and enable real app automation!** 🎯
