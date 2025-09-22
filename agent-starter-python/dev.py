#!/usr/bin/env python3
"""
Development workflow script for LiveKit Agent Starter
Provides common development tasks and shortcuts.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, interactive=False):
    """Run a command"""
    if interactive:
        return os.system(cmd)
    else:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {cmd}")
            print(f"Error: {e.stderr}")
            return None

def check_setup():
    """Run setup verification"""
    print("🔍 Running setup check...")
    result = subprocess.run(["uv", "run", "python", "setup_check.py"])
    return result.returncode == 0

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    return run_command("uv run pytest -v", interactive=True)

def run_linting():
    """Run code linting"""
    print("🔍 Running linting...")
    return run_command("uv run ruff check src/ tests/", interactive=True)

def format_code():
    """Format code"""
    print("✨ Formatting code...")
    return run_command("uv run ruff format src/ tests/", interactive=True)

def console_mode():
    """Run agent in console mode"""
    print("🎤 Starting agent in console mode...")
    print("Speak to test the voice AI agent directly!")
    print("Press Ctrl+C to stop")
    return run_command("uv run python src/agent.py console", interactive=True)

def dev_mode():
    """Run agent in development mode"""
    print("🔧 Starting agent in development mode...")
    print("Agent ready for frontend/telephony connections")
    print("Press Ctrl+C to stop")
    return run_command("uv run python src/agent.py dev", interactive=True)

def download_models():
    """Download required models"""
    print("📥 Downloading models...")
    return run_command("uv run python src/agent.py download-files", interactive=True)

def show_logs():
    """Show recent logs (if any)"""
    print("📋 Recent logs:")
    # This is a placeholder - actual log location depends on configuration
    log_files = [
        Path("agent.log"),
        Path("logs/agent.log"),
        Path("/tmp/livekit-agent.log")
    ]
    
    for log_file in log_files:
        if log_file.exists():
            print(f"📄 {log_file}:")
            print(log_file.read_text()[-1000:])  # Last 1000 chars
            return
    
    print("No log files found")

def main():
    parser = argparse.ArgumentParser(description="LiveKit Agent Development Tools")
    parser.add_argument(
        "command",
        choices=[
            "check", "test", "lint", "format", "console", 
            "dev", "models", "logs", "all-checks"
        ],
        help="Development command to run"
    )
    
    args = parser.parse_args()
    
    print("🛠️  LiveKit Agent Development Tools")
    print("=" * 35)
    
    if args.command == "check":
        success = check_setup()
        sys.exit(0 if success else 1)
    
    elif args.command == "test":
        run_tests()
    
    elif args.command == "lint":
        run_linting()
    
    elif args.command == "format":
        format_code()
    
    elif args.command == "console":
        if not check_setup():
            print("❌ Setup check failed. Fix configuration first.")
            sys.exit(1)
        console_mode()
    
    elif args.command == "dev":
        if not check_setup():
            print("❌ Setup check failed. Fix configuration first.")
            sys.exit(1)
        dev_mode()
    
    elif args.command == "models":
        download_models()
    
    elif args.command == "logs":
        show_logs()
    
    elif args.command == "all-checks":
        print("🔍 Running all checks...")
        
        checks = [
            ("Setup Check", check_setup),
            ("Linting", lambda: run_linting() == 0),
            ("Tests", lambda: run_tests() == 0),
        ]
        
        all_passed = True
        for name, check_func in checks:
            try:
                passed = check_func()
                status = "✅" if passed else "❌"
                print(f"{status} {name}")
                if not passed:
                    all_passed = False
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
                all_passed = False
        
        print("\n" + "=" * 35)
        if all_passed:
            print("🎉 All checks passed!")
        else:
            print("⚠️  Some checks failed.")
        
        sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("🛠️  LiveKit Agent Development Tools")
        print("=" * 35)
        print("\nAvailable commands:")
        print("  check      - Run setup verification")
        print("  test       - Run test suite")
        print("  lint       - Run code linting")
        print("  format     - Format code")
        print("  console    - Test agent in console mode")
        print("  dev        - Run agent in development mode")
        print("  models     - Download required models")
        print("  logs       - Show recent logs")
        print("  all-checks - Run all verification checks")
        print("\nExample: python dev.py console")
        sys.exit(0)
    
    main()
