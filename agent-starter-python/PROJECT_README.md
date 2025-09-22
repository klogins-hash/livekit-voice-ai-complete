# LiveKit Voice AI Agent - Production Ready with RUBE Integration

A complete voice AI assistant built with LiveKit Agents for Python, now with **500+ app integrations** through RUBE MCP, ready for production deployment.

## 🚀 Quick Start

### 1. Configure Environment
```bash
# Interactive configuration
uv run python configure_env.py

# Or manually edit .env.local with your API keys
```

### 2. Verify Setup
```bash
uv run python setup_check.py
```

### 3. Test the Agent
```bash
# Console mode (speak directly to agent)
uv run python dev.py console

# Development mode (for frontend integration)
uv run python dev.py dev
```

## 📋 Development Tools

This project includes several helper scripts for development:

### `dev.py` - Development Workflow
```bash
python dev.py check        # Verify setup
python dev.py test         # Run tests
python dev.py lint         # Code linting
python dev.py format       # Format code
python dev.py console      # Test in console mode
python dev.py dev          # Run in dev mode
python dev.py all-checks   # Run all verifications
```

### `configure_env.py` - Environment Setup
Interactive script to configure all required API keys:
- LiveKit Cloud credentials
- OpenAI API key
- Deepgram API key  
- Cartesia API key

### `setup_check.py` - Setup Verification
Verifies that all dependencies and configuration are correct.

### `deploy.py` - Deployment Helper
```bash
python deploy.py local     # Local deployment
python deploy.py build     # Build Docker image
python deploy.py docker    # Deploy with Docker
```

## 🏗️ Project Structure

```
agent-starter-python/
├── src/
│   └── agent.py              # Main voice AI agent
├── tests/                    # Test suite
├── .env.local               # Environment variables (create this)
├── .env.example             # Example environment file
├── configure_env.py         # Interactive env setup
├── setup_check.py           # Setup verification
├── dev.py                   # Development tools
├── deploy.py                # Deployment helper
├── SETUP_GUIDE.md           # Detailed setup guide
├── PROJECT_README.md        # This file
├── Dockerfile               # Production deployment
└── pyproject.toml           # Python configuration
```

## 🔑 Required API Keys

Get these API keys and configure them using `configure_env.py`:

1. **LiveKit Cloud**: [https://cloud.livekit.io/](https://cloud.livekit.io/)
   - LIVEKIT_URL
   - LIVEKIT_API_KEY
   - LIVEKIT_API_SECRET

2. **OpenAI**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - OPENAI_API_KEY

3. **Deepgram**: [https://console.deepgram.com/](https://console.deepgram.com/)
   - DEEPGRAM_API_KEY

4. **Cartesia**: [https://play.cartesia.ai/keys](https://play.cartesia.ai/keys)
   - CARTESIA_API_KEY

## 🚀 Deployment Options

### Local Development
```bash
python deploy.py local
```

### Docker Deployment
```bash
# Build and run
python deploy.py docker

# Build only
python deploy.py build

# Interactive mode
python deploy.py docker --interactive
```

### Production Deployment
```bash
# Direct production start
uv run python src/agent.py start

# Or use Docker in production
docker run --env-file .env.local livekit-agent
```

## 🌐 Frontend Integration

Compatible with multiple frontend frameworks:

- **Web**: [React/Next.js](https://github.com/livekit-examples/agent-starter-react)
- **iOS/macOS**: [Swift](https://github.com/livekit-examples/agent-starter-swift)
- **Android**: [Kotlin](https://github.com/livekit-examples/agent-starter-android)
- **Flutter**: [Cross-platform](https://github.com/livekit-examples/agent-starter-flutter)
- **React Native**: [Mobile](https://github.com/livekit-examples/voice-assistant-react-native)
- **Web Embed**: [Widget](https://github.com/livekit-examples/agent-starter-embed)

## 🧪 Testing

```bash
# Run all tests
python dev.py test

# Run specific tests
uv run pytest tests/test_agent.py -v

# Run all checks (setup, lint, tests)
python dev.py all-checks
```

## 🔧 Customization

### Modify the Agent
Edit `src/agent.py` to:
- Change assistant instructions
- Add new function tools
- Swap AI providers (LLM, STT, TTS)
- Integrate with OpenAI Realtime API

### Alternative Providers
The agent supports various AI providers:
- **LLM**: OpenAI, Anthropic, Google, Azure
- **STT**: Deepgram, Azure, Google, AssemblyAI
- **TTS**: Cartesia, ElevenLabs, Azure, Google

See [LiveKit integrations](https://docs.livekit.io/agents/integrations/) for details.

## 📞 Telephony Support

For phone call integration, see the [LiveKit Telephony docs](https://docs.livekit.io/agents/start/telephony/).

## 🆘 Troubleshooting

### Common Issues

1. **API Key Errors**: Run `python configure_env.py` to set up keys
2. **Setup Issues**: Run `python setup_check.py` to diagnose
3. **Model Issues**: Run `python dev.py models` to re-download
4. **Permission Errors**: Ensure microphone access for console mode

### Getting Help

- [LiveKit Documentation](https://docs.livekit.io/)
- [LiveKit Discord](https://livekit.io/discord)
- [GitHub Issues](https://github.com/livekit-examples/agent-starter-python/issues)

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🎯 Next Steps

1. **Configure API Keys**: `python configure_env.py`
2. **Test Locally**: `python dev.py console`
3. **Deploy**: `python deploy.py docker`
4. **Integrate Frontend**: Choose from the frontend options above
5. **Customize**: Modify `src/agent.py` for your use case

**Ready to build amazing voice AI experiences!** 🎉
