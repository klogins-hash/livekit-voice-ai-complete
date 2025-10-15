#!/bin/bash

# LiveKit Voice AI - Northflank Deployment Script
# This script deploys the complete LiveKit Voice AI stack to Northflank

set -e

echo "🚀 Deploying LiveKit Voice AI to Northflank..."

# Check if Northflank CLI is installed
if ! command -v northflank &> /dev/null; then
    echo "❌ Northflank CLI not found. Please install it first:"
    echo "   npm install -g @northflank/cli"
    exit 1
fi

# Check if user is logged in
if ! northflank whoami &> /dev/null; then
    echo "❌ Not logged in to Northflank. Please run:"
    echo "   northflank login"
    exit 1
fi

# Set project variables
PROJECT_NAME="livekit-voice-ai"
REGION="us-east"

echo "📋 Project: $PROJECT_NAME"
echo "🌍 Region: $REGION"

# Create project if it doesn't exist
echo "🏗️  Creating project..."
northflank create project \
    --name "$PROJECT_NAME" \
    --description "LiveKit Voice AI Complete Stack" \
    --region "$REGION" \
    --color "#002cf2" || echo "Project may already exist"

# Deploy using the configuration file
echo "📦 Deploying services..."
northflank deploy \
    --file northflank-livekit.json \
    --project "$PROJECT_NAME"

echo "🔐 Setting up secrets..."
echo "Please set the following secrets in the Northflank dashboard:"
echo "  - LIVEKIT_API_KEY"
echo "  - LIVEKIT_API_SECRET" 
echo "  - LIVEKIT_URL"
echo "  - OPENAI_API_KEY"
echo "  - DEEPGRAM_API_KEY"
echo "  - CARTESIA_API_KEY"
echo "  - RUBE_API_KEY"

echo ""
echo "✅ Deployment initiated successfully!"
echo "🌐 Check your deployment status at: https://app.northflank.com/projects/$PROJECT_NAME"
echo ""
echo "📝 Next steps:"
echo "  1. Set up the required secrets in the Northflank dashboard"
echo "  2. Configure your custom domain in the service settings"
echo "  3. Monitor the deployment logs for any issues"
echo "  4. Test the voice AI functionality once deployed"
