#!/usr/bin/env python3
"""
Environment synchronization script for LiveKit Agent and Frontend
This script helps sync LiveKit credentials between the agent and frontend projects.
"""

import os
import sys
from pathlib import Path

def load_env_file(file_path):
    """Load environment variables from a file"""
    env_vars = {}
    if file_path.exists():
        for line in file_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
    return env_vars

def save_env_file(file_path, env_vars, template_content=None):
    """Save environment variables to a file"""
    if template_content:
        content = template_content.format(**env_vars)
    else:
        content = '\n'.join([f"{key}={value}" for key, value in env_vars.items()])
    
    file_path.write_text(content)

def main():
    """Sync environment variables between agent and frontend"""
    print("🔄 LiveKit Environment Synchronization")
    print("=" * 40)
    
    # Define paths
    agent_env = Path("agent-starter-python/.env.local")
    frontend_env = Path("agent-starter-react/.env.local")
    
    # Check if agent env exists
    if not agent_env.exists():
        print("❌ Agent .env.local not found!")
        print("Please run the agent configuration first:")
        print("  cd agent-starter-python")
        print("  uv run python configure_env.py")
        sys.exit(1)
    
    # Load agent environment
    agent_vars = load_env_file(agent_env)
    
    # Check required variables
    required_vars = ['LIVEKIT_URL', 'LIVEKIT_API_KEY', 'LIVEKIT_API_SECRET']
    missing_vars = [var for var in required_vars if var not in agent_vars or agent_vars[var].startswith('your_')]
    
    if missing_vars:
        print(f"❌ Missing or placeholder values in agent config: {', '.join(missing_vars)}")
        print("Please configure the agent first:")
        print("  cd agent-starter-python")
        print("  uv run python configure_env.py")
        sys.exit(1)
    
    # Create frontend environment
    frontend_template = """# LiveKit Configuration
# These values are synced from the agent configuration
LIVEKIT_API_KEY={LIVEKIT_API_KEY}
LIVEKIT_API_SECRET={LIVEKIT_API_SECRET}
LIVEKIT_URL={LIVEKIT_URL}

# Internal environment variables (leave as is)
NEXT_PUBLIC_APP_CONFIG_ENDPOINT=
SANDBOX_ID="""
    
    frontend_vars = {
        'LIVEKIT_URL': agent_vars['LIVEKIT_URL'],
        'LIVEKIT_API_KEY': agent_vars['LIVEKIT_API_KEY'],
        'LIVEKIT_API_SECRET': agent_vars['LIVEKIT_API_SECRET']
    }
    
    save_env_file(frontend_env, frontend_vars, frontend_template)
    
    print("✅ Environment variables synchronized!")
    print()
    print("📋 Synced variables:")
    for var in required_vars:
        value = agent_vars[var]
        display_value = value[:8] + '...' if len(value) > 8 else value
        print(f"  • {var}: {display_value}")
    
    print()
    print("🚀 Next steps:")
    print("  1. Start the agent: cd agent-starter-python && python deploy.py local")
    print("  2. Start the frontend: cd agent-starter-react && pnpm dev")
    print("  3. Open http://localhost:3000 in your browser")

if __name__ == "__main__":
    main()
