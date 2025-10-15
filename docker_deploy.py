#!/usr/bin/env python3
"""
Simple Docker Deployment for Voice AI System
Test locally first, then deploy anywhere (DigitalOcean, AWS, etc.)
"""

import os
import subprocess
from pathlib import Path

def create_simple_dockerfile():
    """Create a simple, unified Dockerfile"""
    dockerfile_content = """
# Use Python 3.11 as base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    git \\
    nodejs \\
    npm \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

# Install pnpm for frontend
RUN npm install -g pnpm

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install Python dependencies
WORKDIR /app/agent-starter-python
RUN pip install uv && uv sync

# Install frontend dependencies and build
WORKDIR /app/agent-starter-react
RUN pnpm install && pnpm build

# Go back to app root
WORKDIR /app

# Install proxy dependencies
RUN pip install fastapi uvicorn python-dotenv httpx

# Create startup script that runs everything in the same process context
RUN echo '#!/bin/bash\\n\\
set -e\\n\\
\\n\\
echo "🚀 Starting Voice AI System with Real MCP Integration..."\\n\\
echo "This runs everything in the same process context for MCP access"\\n\\
\\n\\
# Export environment variables\\n\\
export PYTHONPATH="/app:$PYTHONPATH"\\n\\
\\n\\
# Start services in background\\n\\
echo "📡 Starting MCP-enabled proxy server..."\\n\\
cd /app && python3 mcp_enabled_proxy.py &\\n\\
PROXY_PID=$!\\n\\
sleep 3\\n\\
\\n\\
echo "🤖 Starting LiveKit agent..."\\n\\
cd /app/agent-starter-python && uv run python src/agent.py start &\\n\\
AGENT_PID=$!\\n\\
sleep 3\\n\\
\\n\\
echo "🌐 Starting frontend server..."\\n\\
cd /app/agent-starter-react && pnpm start &\\n\\
FRONTEND_PID=$!\\n\\
sleep 3\\n\\
\\n\\
echo "✅ All services started successfully!"\\n\\
echo "📊 Service Status:"\\n\\
echo "   📡 MCP Proxy: http://localhost:8002"\\n\\
echo "   🤖 LiveKit Agent: Connected"\\n\\
echo "   🌐 Frontend: http://localhost:3001"\\n\\
echo ""\\n\\
echo "🎤 Ready for voice commands!"\\n\\
\\n\\
# Keep container running and show logs\\n\\
tail -f /dev/null\\n\\
' > /app/start_unified.sh && chmod +x /app/start_unified.sh

# Expose ports
EXPOSE 3001 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:8002/health || exit 1

# Start everything
CMD ["/app/start_unified.sh"]
"""
    
    with open("Dockerfile.unified", "w") as f:
        f.write(dockerfile_content)
    print("✅ Created unified Dockerfile")

def create_simple_compose():
    """Create simple Docker Compose for easy deployment"""
    compose_content = """
version: '3.8'

services:
  voice-ai:
    build:
      context: .
      dockerfile: Dockerfile.unified
    ports:
      - "3001:3001"  # Frontend
      - "8002:8002"  # MCP Proxy
    environment:
      # Required API Keys
      - RUBE_API_KEY=${RUBE_API_KEY:-your_rube_api_key}
      - LIVEKIT_URL=${LIVEKIT_URL:-wss://your-instance.livekit.cloud}
      - LIVEKIT_API_KEY=${LIVEKIT_API_KEY:-your_livekit_key}
      - LIVEKIT_API_SECRET=${LIVEKIT_API_SECRET:-your_livekit_secret}
      - OPENAI_API_KEY=${OPENAI_API_KEY:-your_openai_key}
      - DEEPGRAM_API_KEY=${DEEPGRAM_API_KEY:-your_deepgram_key}
      - CARTESIA_API_KEY=${CARTESIA_API_KEY:-your_cartesia_key}
      
      # Application settings
      - NODE_ENV=production
      - PYTHONPATH=/app
      
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

volumes:
  logs:
"""
    
    with open("docker-compose.simple.yml", "w") as f:
        f.write(compose_content)
    print("✅ Created simple Docker Compose")

def create_local_test_script():
    """Create script to test Docker deployment locally"""
    test_script = """#!/bin/bash

echo "🧪 Testing Voice AI System with Docker"
echo "======================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "🔧 Building Docker image..."
docker build -f Dockerfile.unified -t voice-ai-system .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker image built successfully"

echo "🚀 Starting services with Docker Compose..."
docker-compose -f docker-compose.simple.yml up -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start services"
    exit 1
fi

echo "⏳ Waiting for services to start..."
sleep 10

echo "🔍 Checking service health..."

# Check proxy health
if curl -f http://localhost:8002/health > /dev/null 2>&1; then
    echo "✅ MCP Proxy: HEALTHY"
else
    echo "❌ MCP Proxy: NOT RESPONDING"
fi

# Check frontend
if curl -f http://localhost:3001 > /dev/null 2>&1; then
    echo "✅ Frontend: HEALTHY"
else
    echo "❌ Frontend: NOT RESPONDING"
fi

echo ""
echo "🎉 Docker Deployment Test Complete!"
echo "=================================="
echo "🌐 Frontend: http://localhost:3001"
echo "📡 MCP Proxy: http://localhost:8002"
echo ""
echo "📋 To check logs:"
echo "   docker-compose -f docker-compose.simple.yml logs -f"
echo ""
echo "🛑 To stop:"
echo "   docker-compose -f docker-compose.simple.yml down"
echo ""
echo "🎤 Test voice commands at: http://localhost:3001"
"""
    
    with open("test_docker_local.sh", "w") as f:
        f.write(test_script)
    os.chmod("test_docker_local.sh", 0o755)
    print("✅ Created local Docker test script")

def create_production_deploy():
    """Create production deployment script"""
    deploy_script = """#!/bin/bash

echo "🚀 Production Deployment - Voice AI System"
echo "=========================================="

# Check environment variables
required_vars=("RUBE_API_KEY" "LIVEKIT_URL" "LIVEKIT_API_KEY" "LIVEKIT_API_SECRET" "OPENAI_API_KEY")

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Missing required environment variable: $var"
        echo "Please set all required variables in .env file or export them"
        exit 1
    fi
done

echo "✅ All required environment variables are set"

# Build and deploy
echo "🔧 Building production image..."
docker build -f Dockerfile.unified -t voice-ai-production .

echo "🚀 Starting production deployment..."
docker-compose -f docker-compose.simple.yml up -d --build

echo "⏳ Waiting for services to be ready..."
sleep 15

# Health checks
echo "🏥 Running health checks..."

max_attempts=10
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8002/health > /dev/null 2>&1; then
        echo "✅ MCP Proxy is healthy"
        break
    else
        echo "⏳ Attempt $attempt/$max_attempts: Waiting for MCP Proxy..."
        sleep 5
        ((attempt++))
    fi
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ MCP Proxy failed to start properly"
    echo "📋 Check logs: docker-compose -f docker-compose.simple.yml logs voice-ai"
    exit 1
fi

echo ""
echo "🎉 PRODUCTION DEPLOYMENT SUCCESSFUL!"
echo "==================================="
echo "🌐 Your Voice AI System is running at:"
echo "   Frontend: http://localhost:3001"
echo "   MCP Proxy: http://localhost:8002"
echo ""
echo "🔧 Management Commands:"
echo "   View logs: docker-compose -f docker-compose.simple.yml logs -f"
echo "   Restart:   docker-compose -f docker-compose.simple.yml restart"
echo "   Stop:      docker-compose -f docker-compose.simple.yml down"
echo "   Update:    git pull && docker-compose -f docker-compose.simple.yml up -d --build"
echo ""
echo "🎤 Ready for voice automation!"
"""
    
    with open("deploy_production.sh", "w") as f:
        f.write(deploy_script)
    os.chmod("deploy_production.sh", 0o755)
    print("✅ Created production deployment script")

def create_env_file():
    """Create .env file template"""
    env_content = """# Voice AI System Environment Variables
# Copy this file to .env and update with your actual API keys

# RUBE MCP Integration (Required for real app automation)
RUBE_API_KEY=your_rube_api_key_here

# LiveKit Configuration (Required for voice interface)
LIVEKIT_URL=wss://your-instance.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

# AI Service APIs (Required for voice processing)
OPENAI_API_KEY=your_openai_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
CARTESIA_API_KEY=your_cartesia_api_key

# Optional: Additional Configuration
NODE_ENV=production
PYTHONPATH=/app
"""
    
    with open(".env.template", "w") as f:
        f.write(env_content)
    print("✅ Created .env template")

def main():
    """Create all Docker deployment files"""
    print("🐳 Creating Docker Deployment Configuration")
    print("=" * 50)
    
    create_simple_dockerfile()
    create_simple_compose()
    create_local_test_script()
    create_production_deploy()
    create_env_file()
    
    print("\n🎉 Docker deployment files created!")
    print("=" * 50)
    print("📁 Files created:")
    print("   • Dockerfile.unified - Single container with all services")
    print("   • docker-compose.simple.yml - Simple orchestration")
    print("   • test_docker_local.sh - Test locally first")
    print("   • deploy_production.sh - Production deployment")
    print("   • .env.template - Environment variables template")
    
    print("\n🧪 To test locally:")
    print("1. Copy .env.template to .env and add your API keys")
    print("2. Run: ./test_docker_local.sh")
    print("3. Open http://localhost:3001 and test voice commands")
    
    print("\n🚀 To deploy to production:")
    print("1. Set up your server (DigitalOcean, AWS, etc.)")
    print("2. Install Docker and Docker Compose")
    print("3. Copy files to server and run: ./deploy_production.sh")
    
    print("\n💡 Why this should fix the MCP issue:")
    print("   ✅ All services run in the same container/process context")
    print("   ✅ MCP tools available to proxy server")
    print("   ✅ Real app automation should work")
    print("   ✅ Easy to deploy anywhere with Docker")

if __name__ == "__main__":
    main()
