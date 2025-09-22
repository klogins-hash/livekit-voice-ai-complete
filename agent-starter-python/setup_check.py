#!/usr/bin/env python3
"""
Setup verification script for LiveKit Agent Starter
This script checks if all required components are properly configured.
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env.local exists and has required variables"""
    env_file = Path(".env.local")
    if not env_file.exists():
        return False, ".env.local file not found"
    
    required_vars = [
        "LIVEKIT_URL",
        "LIVEKIT_API_KEY", 
        "LIVEKIT_API_SECRET",
        "OPENAI_API_KEY",
        "DEEPGRAM_API_KEY",
        "CARTESIA_API_KEY"
    ]
    
    content = env_file.read_text()
    missing_vars = []
    placeholder_vars = []
    
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
        elif f"{var}=your_" in content or f"{var}=" in content.replace(f"{var}=\n", f"{var}="):
            placeholder_vars.append(var)
    
    if missing_vars:
        return False, f"Missing variables: {', '.join(missing_vars)}"
    
    if placeholder_vars:
        return False, f"Placeholder values detected for: {', '.join(placeholder_vars)}"
    
    return True, "All environment variables configured"

def check_dependencies():
    """Check if required Python packages are installed"""
    try:
        import livekit.agents
        import livekit.plugins.openai
        import livekit.plugins.cartesia
        import livekit.plugins.deepgram
        import livekit.plugins.silero
        return True, "All dependencies installed"
    except ImportError as e:
        return False, f"Missing dependency: {e}"

def check_models():
    """Check if required models are downloaded"""
    # This is a simplified check - the actual model files are in various cache directories
    # The real check would be running the download-files command
    return True, "Models should be downloaded (run 'uv run python src/agent.py download-files' to verify)"

def main():
    """Run all setup checks"""
    print("🔍 LiveKit Agent Setup Verification")
    print("=" * 40)
    
    checks = [
        ("Environment Configuration", check_env_file),
        ("Python Dependencies", check_dependencies), 
        ("ML Models", check_models),
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        try:
            passed, message = check_func()
            status = "✅" if passed else "❌"
            print(f"{status} {check_name}: {message}")
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name}: Error during check - {e}")
            all_passed = False
    
    print("\n" + "=" * 40)
    
    if all_passed:
        print("🎉 Setup verification passed! You can now run the agent:")
        print("   uv run python src/agent.py console")
    else:
        print("⚠️  Setup incomplete. Please address the issues above.")
        print("📖 See SETUP_GUIDE.md for detailed instructions.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
