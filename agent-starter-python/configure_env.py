#!/usr/bin/env python3
"""
Interactive environment configuration script for LiveKit Agent Starter
This script helps you set up all required API keys and configuration.
"""

import os
import sys
from pathlib import Path

def get_user_input(prompt, current_value=None, required=True):
    """Get user input with optional current value display"""
    if current_value and not current_value.startswith('your_'):
        display_value = current_value[:8] + '...' if len(current_value) > 8 else current_value
        prompt += f" (current: {display_value})"
    
    if not required:
        prompt += " (optional)"
    
    prompt += ": "
    
    value = input(prompt).strip()
    
    if not value and current_value and not current_value.startswith('your_'):
        return current_value
    
    if required and not value:
        print("❌ This field is required!")
        return get_user_input(prompt.split(':')[0], current_value, required)
    
    return value

def load_env_file():
    """Load current environment variables from .env.local"""
    env_file = Path(".env.local")
    env_vars = {}
    
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    
    return env_vars

def save_env_file(env_vars):
    """Save environment variables to .env.local"""
    env_content = """# LiveKit Configuration
# Get these from LiveKit Cloud (https://cloud.livekit.io/) or your self-hosted instance
LIVEKIT_URL={LIVEKIT_URL}
LIVEKIT_API_KEY={LIVEKIT_API_KEY}
LIVEKIT_API_SECRET={LIVEKIT_API_SECRET}

# AI Service API Keys
# OpenAI API Key - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY={OPENAI_API_KEY}

# Deepgram API Key - Get from https://console.deepgram.com/
DEEPGRAM_API_KEY={DEEPGRAM_API_KEY}

# Cartesia API Key - Get from https://play.cartesia.ai/keys
CARTESIA_API_KEY={CARTESIA_API_KEY}
""".format(**env_vars)
    
    Path(".env.local").write_text(env_content)

def main():
    """Main configuration flow"""
    print("🔧 LiveKit Agent Environment Configuration")
    print("=" * 50)
    print()
    print("This script will help you configure all required API keys.")
    print("You can get these keys from the following services:")
    print()
    print("📋 Required Services:")
    print("  • LiveKit Cloud: https://cloud.livekit.io/")
    print("  • OpenAI: https://platform.openai.com/api-keys")
    print("  • Deepgram: https://console.deepgram.com/")
    print("  • Cartesia: https://play.cartesia.ai/keys")
    print()
    
    # Load current values
    current_env = load_env_file()
    
    # Configuration sections
    print("🌐 LiveKit Configuration")
    print("-" * 25)
    
    livekit_url = get_user_input(
        "LiveKit URL (e.g., wss://your-project.livekit.cloud)",
        current_env.get('LIVEKIT_URL', '')
    )
    
    livekit_api_key = get_user_input(
        "LiveKit API Key",
        current_env.get('LIVEKIT_API_KEY', '')
    )
    
    livekit_api_secret = get_user_input(
        "LiveKit API Secret",
        current_env.get('LIVEKIT_API_SECRET', '')
    )
    
    print("\n🤖 AI Service API Keys")
    print("-" * 25)
    
    openai_api_key = get_user_input(
        "OpenAI API Key",
        current_env.get('OPENAI_API_KEY', '')
    )
    
    deepgram_api_key = get_user_input(
        "Deepgram API Key",
        current_env.get('DEEPGRAM_API_KEY', '')
    )
    
    cartesia_api_key = get_user_input(
        "Cartesia API Key",
        current_env.get('CARTESIA_API_KEY', '')
    )
    
    # Save configuration
    env_vars = {
        'LIVEKIT_URL': livekit_url,
        'LIVEKIT_API_KEY': livekit_api_key,
        'LIVEKIT_API_SECRET': livekit_api_secret,
        'OPENAI_API_KEY': openai_api_key,
        'DEEPGRAM_API_KEY': deepgram_api_key,
        'CARTESIA_API_KEY': cartesia_api_key,
    }
    
    print("\n💾 Saving configuration...")
    save_env_file(env_vars)
    
    print("✅ Configuration saved to .env.local")
    print()
    print("🧪 Next steps:")
    print("  1. Verify setup: uv run python setup_check.py")
    print("  2. Test agent: uv run python src/agent.py console")
    print("  3. Run for frontend: uv run python src/agent.py dev")
    print()
    print("📖 For more details, see SETUP_GUIDE.md")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Configuration cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
