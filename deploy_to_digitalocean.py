#!/usr/bin/env python3
"""
DigitalOcean Deployment Script for Voice AI System
Creates a production-ready deployment with proper MCP integration.
"""

import os
import subprocess
import json
from pathlib import Path

def create_dockerfile():
    """Create optimized Dockerfile for production deployment"""
    dockerfile_content = """
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    git \\
    nodejs \\
    npm \\
    && rm -rf /var/lib/apt/lists/*

# Install pnpm
RUN npm install -g pnpm

# Set working directory
WORKDIR /app

# Copy Python requirements and install
COPY agent-starter-python/pyproject.toml /app/agent/pyproject.toml
WORKDIR /app/agent
RUN pip install uv && uv sync

# Copy frontend package.json and install
COPY agent-starter-react/package.json /app/frontend/package.json
WORKDIR /app/frontend
RUN pnpm install

# Copy all application code
WORKDIR /app
COPY . .

# Build frontend
WORKDIR /app/frontend
RUN pnpm build

# Create startup script
WORKDIR /app
RUN echo '#!/bin/bash\\n\\
echo "🚀 Starting Voice AI System with MCP Integration..."\\n\\
\\n\\
# Start MCP-enabled proxy server in background\\n\\
cd /app && python3 mcp_enabled_proxy.py &\\n\\
PROXY_PID=$!\\n\\
\\n\\
# Start LiveKit agent in background\\n\\
cd /app/agent-starter-python && uv run python src/agent.py start &\\n\\
AGENT_PID=$!\\n\\
\\n\\
# Start frontend\\n\\
cd /app/frontend && pnpm start &\\n\\
FRONTEND_PID=$!\\n\\
\\n\\
echo "✅ All services started"\\n\\
echo "📡 Proxy: http://localhost:8002"\\n\\
echo "🤖 Agent: Connected to LiveKit"\\n\\
echo "🌐 Frontend: http://localhost:3001"\\n\\
\\n\\
# Wait for all processes\\n\\
wait $PROXY_PID $AGENT_PID $FRONTEND_PID\\n\\
' > start_all.sh && chmod +x start_all.sh

# Expose ports
EXPOSE 3001 8002

# Start all services
CMD ["./start_all.sh"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    print("✅ Created production Dockerfile")

def create_docker_compose():
    """Create Docker Compose configuration"""
    compose_content = """
version: '3.8'

services:
  voice-ai-system:
    build: .
    ports:
      - "3001:3001"  # Frontend
      - "8002:8002"  # MCP Proxy
    environment:
      - RUBE_API_KEY=${RUBE_API_KEY}
      - LIVEKIT_URL=${LIVEKIT_URL}
      - LIVEKIT_API_KEY=${LIVEKIT_API_KEY}
      - LIVEKIT_API_SECRET=${LIVEKIT_API_SECRET}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DEEPGRAM_API_KEY=${DEEPGRAM_API_KEY}
      - CARTESIA_API_KEY=${CARTESIA_API_KEY}
      - NODE_ENV=production
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Optional: Nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - voice-ai-system
    restart: unless-stopped

volumes:
  logs:
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    print("✅ Created Docker Compose configuration")

def create_nginx_config():
    """Create Nginx configuration for production"""
    nginx_content = """
events {
    worker_connections 1024;
}

http {
    upstream voice_ai {
        server voice-ai-system:3001;
    }
    
    upstream mcp_proxy {
        server voice-ai-system:8002;
    }

    server {
        listen 80;
        server_name your-domain.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;
        
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        
        # Frontend
        location / {
            proxy_pass http://voice_ai;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # MCP Proxy API
        location /api/ {
            proxy_pass http://mcp_proxy/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # WebSocket support for LiveKit
        location /ws {
            proxy_pass http://voice_ai;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }
    }
}
"""
    
    with open("nginx.conf", "w") as f:
        f.write(nginx_content)
    print("✅ Created Nginx configuration")

def create_deployment_script():
    """Create DigitalOcean deployment script"""
    deploy_script = """#!/bin/bash

echo "🚀 Deploying Voice AI System to DigitalOcean"
echo "=============================================="

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo "❌ DigitalOcean CLI (doctl) not found. Please install it first."
    echo "   Install: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Create droplet
echo "📡 Creating DigitalOcean droplet..."
doctl compute droplet create voice-ai-production \\
    --image ubuntu-20-04-x64 \\
    --size s-2vcpu-4gb \\
    --region nyc1 \\
    --ssh-keys $(doctl compute ssh-key list --format ID --no-header | head -1) \\
    --wait

# Get droplet IP
DROPLET_IP=$(doctl compute droplet list voice-ai-production --format PublicIPv4 --no-header)
echo "✅ Droplet created with IP: $DROPLET_IP"

# Wait for droplet to be ready
echo "⏳ Waiting for droplet to be ready..."
sleep 30

# Setup droplet
echo "🔧 Setting up droplet..."
ssh -o StrictHostKeyChecking=no root@$DROPLET_IP << 'EOF'
    # Update system
    apt update && apt upgrade -y
    
    # Install Docker
    apt install -y docker.io docker-compose
    systemctl start docker
    systemctl enable docker
    
    # Install Git
    apt install -y git curl
    
    echo "✅ Droplet setup complete"
EOF

# Deploy application
echo "📦 Deploying application..."
scp -r . root@$DROPLET_IP:/root/voice-ai-system/

ssh root@$DROPLET_IP << 'EOF'
    cd /root/voice-ai-system
    
    # Set environment variables (you'll need to update these)
    export RUBE_API_KEY="your_rube_api_key"
    export LIVEKIT_URL="wss://your-instance.livekit.cloud"
    export LIVEKIT_API_KEY="your_livekit_api_key"
    export LIVEKIT_API_SECRET="your_livekit_api_secret"
    export OPENAI_API_KEY="your_openai_api_key"
    export DEEPGRAM_API_KEY="your_deepgram_api_key"
    export CARTESIA_API_KEY="your_cartesia_api_key"
    
    # Build and start services
    docker-compose up -d --build
    
    echo "✅ Application deployed successfully!"
    echo "🌐 Frontend: http://$DROPLET_IP:3001"
    echo "📡 MCP Proxy: http://$DROPLET_IP:8002"
EOF

echo ""
echo "🎉 Deployment Complete!"
echo "======================="
echo "🌐 Your Voice AI System is now running at:"
echo "   Frontend: http://$DROPLET_IP:3001"
echo "   MCP Proxy: http://$DROPLET_IP:8002"
echo ""
echo "📝 Next Steps:"
echo "1. Update your DNS to point to $DROPLET_IP"
echo "2. Set up SSL certificates"
echo "3. Configure your API keys in the environment"
echo "4. Test the voice automation functionality"
"""
    
    with open("deploy_digitalocean.sh", "w") as f:
        f.write(deploy_script)
    os.chmod("deploy_digitalocean.sh", 0o755)
    print("✅ Created DigitalOcean deployment script")

def create_env_template():
    """Create environment template for production"""
    env_content = """# Production Environment Variables
# Copy this to .env and fill in your actual values

# RUBE MCP Integration
RUBE_API_KEY=your_rube_api_key_here

# LiveKit Configuration
LIVEKIT_URL=wss://your-instance.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret

# AI Service APIs
OPENAI_API_KEY=your_openai_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
CARTESIA_API_KEY=your_cartesia_api_key

# Application Configuration
NODE_ENV=production
PORT=3001
MCP_PROXY_PORT=8002

# Optional: Database (if needed)
# DATABASE_URL=postgresql://user:pass@localhost:5432/voiceai
"""
    
    with open(".env.production", "w") as f:
        f.write(env_content)
    print("✅ Created production environment template")

def main():
    """Create all deployment files"""
    print("🚀 Creating DigitalOcean Deployment Configuration")
    print("=" * 50)
    
    create_dockerfile()
    create_docker_compose()
    create_nginx_config()
    create_deployment_script()
    create_env_template()
    
    print("\n🎉 Deployment files created successfully!")
    print("=" * 50)
    print("📁 Files created:")
    print("   • Dockerfile - Production container configuration")
    print("   • docker-compose.yml - Service orchestration")
    print("   • nginx.conf - Reverse proxy configuration")
    print("   • deploy_digitalocean.sh - Automated deployment script")
    print("   • .env.production - Environment variables template")
    
    print("\n🚀 To deploy to DigitalOcean:")
    print("1. Update .env.production with your API keys")
    print("2. Install DigitalOcean CLI: doctl")
    print("3. Run: ./deploy_digitalocean.sh")
    
    print("\n💡 This deployment should fix the MCP integration issue by:")
    print("   ✅ Running all services in the same container environment")
    print("   ✅ Ensuring MCP context is available to all processes")
    print("   ✅ Providing proper production configuration")
    print("   ✅ Enabling real app automation through RUBE MCP")

if __name__ == "__main__":
    main()
