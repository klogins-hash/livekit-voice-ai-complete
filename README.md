# 🎤 LiveKit Voice AI Complete - Full Stack Voice Automation

A complete voice AI system with **real app automation** capabilities. Talk to your AI agent and have it actually send emails, create documents, post to social media, and automate workflows across 500+ apps.

## 🌟 Features

- **🎤 Voice AI Agent**: OpenAI-powered conversational AI with LiveKit
- **🌐 React Frontend**: Modern web interface with audio visualization
- **🤖 Real App Automation**: Actually send emails, create docs, post to social media
- **🔗 500+ App Integrations**: Gmail, Slack, Google Workspace, GitHub, and more
- **🚀 Production Ready**: Docker deployment, comprehensive testing
- **🔒 Secure**: Proper authentication and API key management

## 🏗️ Architecture

```
Voice User → React Frontend → LiveKit Agent → RUBE Proxy → Real Apps
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- pnpm
- API keys for LiveKit, OpenAI, Deepgram, Cartesia, RUBE

### 1. Clone and Setup

```bash
git clone https://github.com/klogins-hash/livekit-voice-ai-complete.git
cd livekit-voice-ai-complete
```

### 2. Configure Agent

```bash
cd agent-starter-python
uv sync
uv run python configure_env.py  # Interactive API key setup
```

### 3. Configure Frontend

```bash
cd ../agent-starter-react
pnpm install
# Environment will be synced automatically
```

### 4. Start the System

**Terminal 1: RUBE Proxy Server**
```bash
python3 rube_proxy_server.py
```

**Terminal 2: LiveKit Agent**
```bash
cd agent-starter-python
uv run python src/agent.py dev
```

**Terminal 3: React Frontend**
```bash
cd agent-starter-react
pnpm dev
```

### 5. Test Voice Automation

Open http://localhost:3001 and try:
- *"Send an email to john@example.com"*
- *"Create a Google Doc called Meeting Notes"*
- *"Post to LinkedIn about our product"*
- *"What apps can you integrate with?"*

## 📁 Project Structure

```
livekit-voice-ai-complete/
├── agent-starter-python/          # Voice AI Agent (Backend)
│   ├── src/
│   │   ├── agent.py               # Main agent with RUBE integration
│   │   ├── proxy_rube_integration.py  # RUBE MCP client
│   │   └── [other modules]
│   ├── configure_env.py           # Interactive setup
│   ├── deploy.py                  # Deployment tools
│   └── pyproject.toml             # Dependencies
├── agent-starter-react/           # React Frontend
│   ├── app/                       # Next.js app
│   ├── components/                # React components
│   └── package.json               # Frontend dependencies
├── rube_proxy_server.py           # RUBE MCP proxy server
├── sync_env.py                    # Environment synchronization
├── start_agent.sh                 # Agent startup script
├── start_frontend.sh              # Frontend startup script
└── [documentation files]
```

## 🎯 Real Automation Examples

### Email Automation
```
User: "Send an email to sarah@company.com about tomorrow's meeting"
Agent: [Searches for email tools] → [Executes Gmail workflow] → "Email sent!"
```

### Document Creation
```
User: "Create a Google Doc called Project Plan"
Agent: [Finds Google Docs tools] → [Creates document] → "Document ready!"
```

### Social Media
```
User: "Post to LinkedIn about our product launch"
Agent: [Locates LinkedIn tools] → [Posts content] → "Posted successfully!"
```

## 🔧 Configuration

### Required API Keys

1. **LiveKit Cloud**: [Get credentials](https://cloud.livekit.io/)
2. **OpenAI**: [Get API key](https://platform.openai.com/api-keys)
3. **Deepgram**: [Get API key](https://console.deepgram.com/)
4. **Cartesia**: [Get API key](https://play.cartesia.ai/keys)
5. **RUBE**: [Contact for MCP access](https://rube.app/)

### Environment Setup

Use the interactive configuration:
```bash
cd agent-starter-python
uv run python configure_env.py
```

Or manually edit `.env.local`:
```env
LIVEKIT_URL=wss://your-instance.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
OPENAI_API_KEY=your_openai_key
DEEPGRAM_API_KEY=your_deepgram_key
CARTESIA_API_KEY=your_cartesia_key
RUBE_API_KEY=Bearer your_rube_token
```

## 🚀 Deployment

### Docker Deployment

```bash
# Build agent
cd agent-starter-python
python3 deploy.py build

# Build frontend
cd ../agent-starter-react
pnpm build

# Deploy with Docker Compose (create docker-compose.yml)
docker-compose up -d
```

### Production Environment

```bash
# Agent production mode
cd agent-starter-python
uv run python src/agent.py start

# Frontend production build
cd agent-starter-react
pnpm build && pnpm start
```

## 🧪 Testing

### Test Agent
```bash
cd agent-starter-python
uv run python setup_check.py      # Verify setup
uv run python test_rube.py        # Test RUBE integration
uv run python dev.py console      # Test voice interaction
```

### Test Frontend
```bash
cd agent-starter-react
pnpm dev  # Start development server
# Open http://localhost:3001
```

## 📚 Documentation

- **[Agent Setup Guide](agent-starter-python/SETUP_GUIDE.md)** - Detailed agent configuration
- **[RUBE Integration Guide](REAL_RUBE_INTEGRATION_GUIDE.md)** - Real app automation setup
- **[Frontend Integration Guide](FRONTEND_INTEGRATION_GUIDE.md)** - Frontend setup and usage
- **[Deployment Guide](agent-starter-python/PROJECT_README.md)** - Production deployment

## 🔒 Security

- API keys stored in environment variables
- Secure token-based authentication
- OAuth flows handled by RUBE platform
- No sensitive data in logs or responses

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/klogins-hash/livekit-voice-ai-complete/issues)
- **LiveKit Docs**: [https://docs.livekit.io/](https://docs.livekit.io/)
- **Community**: [LiveKit Discord](https://livekit.io/discord)

## 🎉 What You Can Do

With this system, you can:

- ✅ **Send emails** through Gmail, Outlook with voice commands
- ✅ **Create and edit documents** in Google Docs, Word
- ✅ **Post to social media** on LinkedIn, Twitter, Facebook
- ✅ **Manage calendars** and schedule meetings
- ✅ **Automate workflows** across 500+ connected apps
- ✅ **Build custom voice interfaces** for any application
- ✅ **Deploy at scale** with production-ready architecture

**Ready to revolutionize how you interact with technology through voice!** 🚀

---

**⭐ Star this repo if you find it useful!**
