# LiveKit Agent Starter - Setup and Deployment Guide

This guide will help you complete the setup and deployment of your LiveKit voice AI agent.

## ✅ Completed Setup Steps

The following steps have been completed for you:

1. **Repository Cloned**: The project has been cloned to `/Users/franksimpson/CascadeProjects/agent-starter-python`
2. **Dependencies Installed**: All Python dependencies have been installed using `uv sync`
3. **Models Downloaded**: Required ML models (Silero VAD, LiveKit turn detector) have been downloaded
4. **Environment File Created**: `.env.local` file has been created with placeholder values

## 🔑 Required API Keys

To run the agent, you need to obtain and configure the following API keys in `.env.local`:

### LiveKit Configuration
- **LIVEKIT_URL**: Get from [LiveKit Cloud](https://cloud.livekit.io/) or [self-host](https://docs.livekit.io/home/self-hosting/)
- **LIVEKIT_API_KEY**: From your LiveKit project
- **LIVEKIT_API_SECRET**: From your LiveKit project

### AI Service API Keys
- **OPENAI_API_KEY**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **DEEPGRAM_API_KEY**: Get from [Deepgram Console](https://console.deepgram.com/)
- **CARTESIA_API_KEY**: Get from [Cartesia](https://play.cartesia.ai/keys)

## 🚀 Next Steps

### 1. Configure API Keys
Edit the `.env.local` file and replace the placeholder values with your actual API keys:

```bash
cd /Users/franksimpson/CascadeProjects/agent-starter-python
# Edit .env.local with your preferred editor
code .env.local  # or nano .env.local
```

### 2. Test the Agent
Once you have valid API keys, test the agent:

```bash
# Test in console mode (speak directly to the agent in terminal)
uv run python src/agent.py console

# Run in development mode (for use with frontend/telephony)
uv run python src/agent.py dev

# Run tests
uv run pytest
```

### 3. Production Deployment Options

#### Option A: Docker Deployment
The project includes a production-ready Dockerfile:

```bash
# Build the Docker image
docker build -t livekit-agent .

# Run the container (make sure to pass environment variables)
docker run --env-file .env.local livekit-agent
```

#### Option B: LiveKit Cloud Deployment
Follow the [LiveKit Cloud deployment guide](https://docs.livekit.io/agents/ops/deployment/) to deploy directly to LiveKit Cloud.

#### Option C: Manual Deployment
For production deployment on your own infrastructure:

```bash
# Use the start command for production
uv run python src/agent.py start
```

## 🌐 Frontend Integration

The agent can be used with various frontend applications:

- **Web**: [React/Next.js starter](https://github.com/livekit-examples/agent-starter-react)
- **iOS/macOS**: [Swift starter](https://github.com/livekit-examples/agent-starter-swift)
- **Android**: [Kotlin starter](https://github.com/livekit-examples/agent-starter-android)
- **Flutter**: [Flutter starter](https://github.com/livekit-examples/agent-starter-flutter)
- **React Native**: [React Native starter](https://github.com/livekit-examples/voice-assistant-react-native)
- **Web Embed**: [Embeddable widget](https://github.com/livekit-examples/agent-starter-embed)

## 📞 Telephony Support

For telephony integration, see the [LiveKit Telephony documentation](https://docs.livekit.io/agents/start/telephony/).

## 🔧 Customization

### Modifying the Agent
The main agent code is in `src/agent.py`. You can:
- Change the assistant's instructions
- Add new function tools
- Swap AI providers (LLM, STT, TTS)
- Integrate with the OpenAI Realtime API

### Alternative AI Providers
The agent supports various providers:
- **LLM**: OpenAI, Anthropic, Google, Azure, and more
- **STT**: Deepgram, Azure, Google, AssemblyAI, and more  
- **TTS**: Cartesia, ElevenLabs, Azure, Google, and more

See the [LiveKit Agents integrations documentation](https://docs.livekit.io/agents/integrations/) for details.

## 🧪 Testing and Evaluation

The project includes a comprehensive test suite:

```bash
# Run all tests
uv run pytest

# Run specific test files
uv run pytest tests/test_agent.py
```

## 📝 Project Structure

```
agent-starter-python/
├── src/
│   ├── __init__.py
│   └── agent.py          # Main agent implementation
├── tests/                # Test suite
├── .env.local           # Environment variables (you need to configure)
├── .env.example         # Example environment file
├── pyproject.toml       # Python project configuration
├── Dockerfile           # Production Docker image
└── README.md           # Original project documentation
```

## 🆘 Troubleshooting

### Common Issues

1. **API Key Errors**: Make sure all API keys in `.env.local` are valid and have sufficient credits
2. **Model Download Issues**: Run `uv run python src/agent.py download-files` if models aren't found
3. **Permission Errors**: Ensure the user has proper permissions to access audio devices for console mode

### Getting Help

- [LiveKit Documentation](https://docs.livekit.io/)
- [LiveKit Discord Community](https://livekit.io/discord)
- [GitHub Issues](https://github.com/livekit-examples/agent-starter-python/issues)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
