# LiveKit Voice AI - Northflank Deployment Guide

This guide walks you through deploying the complete LiveKit Voice AI stack to Northflank with optimized configurations for production use.

## 🏗️ Architecture Overview

The deployment consists of three main services:

1. **Frontend Service** (`livekit-frontend`)
   - Next.js React application
   - Handles user interface and WebRTC connections
   - Auto-scaling: 1-5 instances

2. **Agent Service** (`livekit-agent`) 
   - Python agent with AI capabilities
   - OpenAI (LLM) + Deepgram (STT) + Cartesia (TTS)
   - Auto-scaling: 1-8 instances

3. **MCP Proxy Service** (`mcp-proxy`)
   - Model Context Protocol integration
   - Handles external API integrations
   - Auto-scaling: 1-3 instances

4. **Redis Cache** (`redis-cache`)
   - Session storage and caching
   - Managed addon service

## 📋 Prerequisites

### 1. Install Northflank CLI
```bash
npm install -g @northflank/cli
```

### 2. Login to Northflank
```bash
northflank login
```

### 3. Required API Keys
Gather the following API keys before deployment:

- **LiveKit**: API Key, Secret, and Server URL
- **OpenAI**: API key for LLM functionality
- **Deepgram**: API key for speech-to-text
- **Cartesia**: API key for text-to-speech
- **RUBE**: API key for MCP integrations (optional)

## 🚀 Deployment Steps

### Step 1: Clone and Prepare Repository
```bash
git clone https://github.com/klogins-hash/livekit-voice-ai-complete.git
cd livekit-voice-ai-complete
```

### Step 2: Configure Environment Variables
1. Copy the environment template:
   ```bash
   cp northflank-env-template.yaml northflank-env.yaml
   ```

2. Edit `northflank-env.yaml` with your actual API keys and configuration.

### Step 3: Deploy to Northflank
Run the deployment script:
```bash
./deploy-northflank.sh
```

Or deploy manually using the Northflank CLI:
```bash
northflank deploy --file northflank-livekit.json --project livekit-voice-ai
```

### Step 4: Configure Secrets
In the Northflank dashboard, navigate to your project and set up the following secrets:

#### Required Secrets:
- `LIVEKIT_API_KEY`: Your LiveKit API key
- `LIVEKIT_API_SECRET`: Your LiveKit API secret  
- `LIVEKIT_URL`: Your LiveKit server WebSocket URL (e.g., `wss://your-project.livekit.cloud`)
- `OPENAI_API_KEY`: Your OpenAI API key
- `DEEPGRAM_API_KEY`: Your Deepgram API key
- `CARTESIA_API_KEY`: Your Cartesia API key

#### Optional Secrets:
- `RUBE_API_KEY`: For MCP integrations

### Step 5: Configure Custom Domains (Optional)
1. In the Northflank dashboard, go to your frontend service
2. Navigate to "Networking" → "Domains"
3. Add your custom domain
4. Configure SSL certificate

## 🔧 Configuration Details

### Service Specifications

#### Frontend Service
- **Compute Plan**: `nf-compute-20`
- **Instances**: 1-5 (auto-scaling)
- **Resources**: 500m CPU, 1Gi RAM
- **Port**: 3000
- **Health Check**: `/api/health`

#### Agent Service  
- **Compute Plan**: `nf-compute-30`
- **Instances**: 1-8 (auto-scaling)
- **Resources**: 1000m CPU, 2Gi RAM
- **Port**: 8080
- **Health Check**: `/health`

#### MCP Proxy Service
- **Compute Plan**: `nf-compute-15` 
- **Instances**: 1-3 (auto-scaling)
- **Resources**: 250m CPU, 512Mi RAM
- **Port**: 8002
- **Health Check**: `/health`

### Auto-scaling Configuration
- **CPU Threshold**: 70-75%
- **Memory Threshold**: 80-85%
- **Scale-up**: Gradual based on load
- **Scale-down**: Conservative to maintain performance

### Networking
- **Private Networking**: Enabled for service-to-service communication
- **Internal DNS**: Enabled for service discovery
- **Network Policies**: Configured for security

## 📊 Monitoring and Observability

### Health Checks
- **Frontend**: HTTP health check on `/api/health`
- **Agent**: HTTP health check on `/health` 
- **MCP Proxy**: HTTP health check on `/health`

### Metrics and Alerts
The deployment includes comprehensive monitoring:

- **CPU/Memory Usage**: Alerts at 80%+ CPU, 85%+ memory
- **Service Availability**: Immediate alerts if services go down
- **Response Time**: Monitoring for performance degradation
- **Error Rates**: Tracking application errors

### Logging
- **Structured Logging**: JSON format for better parsing
- **Log Retention**: 30 days
- **Log Aggregation**: Automatic error pattern detection

## 🔒 Security Features

### Container Security
- **Non-root Users**: All containers run as non-privileged users
- **Minimal Base Images**: Using slim/alpine images
- **Security Headers**: Configured in Next.js

### Network Security
- **Private Networking**: Internal service communication
- **Network Policies**: Restricted ingress/egress rules
- **SSL/TLS**: Automatic HTTPS for public endpoints

### Secret Management
- **Encrypted Storage**: All secrets encrypted at rest
- **Environment Isolation**: Secrets scoped to specific services
- **Rotation Support**: Easy secret rotation capabilities

## 🐛 Troubleshooting

### Common Issues

#### 1. Service Won't Start
- Check logs in Northflank dashboard
- Verify all required secrets are set
- Ensure Docker build completed successfully

#### 2. Health Check Failures
- Verify health check endpoints are responding
- Check service startup time vs. initial delay
- Review resource allocation (CPU/memory)

#### 3. LiveKit Connection Issues
- Verify LiveKit credentials are correct
- Check LiveKit server URL format
- Ensure network policies allow external connections

#### 4. AI Service Errors
- Verify API keys for OpenAI, Deepgram, Cartesia
- Check API rate limits and quotas
- Review agent logs for specific errors

### Debugging Commands
```bash
# View service logs
northflank logs service --project livekit-voice-ai --service livekit-frontend

# Check service status
northflank get services --project livekit-voice-ai

# View deployment status
northflank get deployments --project livekit-voice-ai
```

## 📈 Performance Optimization

### Scaling Recommendations
- **Frontend**: Scale based on concurrent users
- **Agent**: Scale based on active voice sessions
- **MCP Proxy**: Usually 1-2 instances sufficient

### Resource Optimization
- Monitor actual resource usage and adjust allocations
- Use horizontal scaling over vertical scaling
- Consider regional deployment for global users

### Cost Optimization
- Use appropriate compute plans for each service
- Enable auto-scaling to reduce costs during low usage
- Monitor addon usage (Redis) and optimize as needed

## 🔄 Updates and Maintenance

### Deployment Updates
1. Push changes to your GitHub repository
2. Northflank will automatically trigger new deployments
3. Monitor deployment progress in the dashboard

### Rolling Updates
- Zero-downtime deployments with rolling updates
- Automatic rollback on deployment failures
- Blue-green deployment option available

### Backup and Recovery
- Database backups handled by managed addons
- Application state is stateless and recoverable
- Configuration and secrets backed up automatically

## 📞 Support

For deployment issues:
1. Check the Northflank documentation
2. Review service logs in the dashboard
3. Contact Northflank support for platform issues
4. Check LiveKit documentation for agent-specific issues

## 🎯 Next Steps

After successful deployment:
1. Test voice AI functionality end-to-end
2. Configure monitoring alerts for your team
3. Set up custom domains and SSL certificates
4. Implement CI/CD pipelines for automated deployments
5. Consider multi-region deployment for better performance
