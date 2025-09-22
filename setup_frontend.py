#!/usr/bin/env python3
"""
Complete frontend setup script for LiveKit Agent integration
This script sets up the React frontend to work with the LiveKit agent.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=check
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def check_prerequisites():
    """Check if all prerequisites are available"""
    print("🔍 Checking prerequisites...")
    
    # Check Node.js
    stdout, stderr, code = run_command("node --version", check=False)
    if code != 0:
        print("❌ Node.js not found. Please install Node.js first.")
        return False
    print(f"✅ Node.js: {stdout}")
    
    # Check pnpm
    stdout, stderr, code = run_command("pnpm --version", check=False)
    if code != 0:
        print("❌ pnpm not found. Please install pnpm first.")
        return False
    print(f"✅ pnpm: {stdout}")
    
    # Check if agent is configured
    agent_env = Path("agent-starter-python/.env.local")
    if not agent_env.exists():
        print("❌ Agent not configured. Please run agent setup first.")
        return False
    
    # Check agent env content
    content = agent_env.read_text()
    if "your_" in content:
        print("❌ Agent has placeholder values. Please configure API keys first.")
        return False
    
    print("✅ Agent configured")
    return True

def setup_frontend():
    """Set up the frontend project"""
    print("\n🚀 Setting up frontend...")
    
    frontend_dir = Path("agent-starter-react")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found. Please clone the frontend first.")
        return False
    
    # Install dependencies
    print("📦 Installing dependencies...")
    stdout, stderr, code = run_command("pnpm install", cwd=frontend_dir)
    if code != 0:
        print(f"❌ Failed to install dependencies: {stderr}")
        return False
    print("✅ Dependencies installed")
    
    # Sync environment variables
    print("🔄 Syncing environment variables...")
    stdout, stderr, code = run_command("python3 ../sync_env.py", cwd=frontend_dir)
    if code != 0:
        print(f"❌ Failed to sync environment: {stderr}")
        return False
    print("✅ Environment synced")
    
    return True

def create_startup_scripts():
    """Create convenient startup scripts"""
    print("\n📝 Creating startup scripts...")
    
    # Create start_agent script
    agent_script = Path("start_agent.py")
    agent_script.write_text("""#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    print("🤖 Starting LiveKit Agent...")
    os.chdir("agent-starter-python")
    
    # Check if configured
    if not Path(".env.local").exists():
        print("❌ Agent not configured. Run: uv run python configure_env.py")
        sys.exit(1)
    
    # Start agent
    try:
        subprocess.run(["python", "deploy.py", "local"], check=True)
    except KeyboardInterrupt:
        print("\\n🛑 Agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    from pathlib import Path
    main()
""")
    agent_script.chmod(0o755)
    
    # Create start_frontend script
    frontend_script = Path("start_frontend.py")
    frontend_script.write_text("""#!/usr/bin/env python3
import os
import subprocess
import sys

def main():
    print("🌐 Starting LiveKit Frontend...")
    os.chdir("agent-starter-react")
    
    # Check if configured
    if not Path(".env.local").exists():
        print("❌ Frontend not configured. Run setup_frontend.py first")
        sys.exit(1)
    
    # Start frontend
    try:
        subprocess.run(["pnpm", "dev"], check=True)
    except KeyboardInterrupt:
        print("\\n🛑 Frontend stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    from pathlib import Path
    main()
""")
    frontend_script.chmod(0o755)
    
    # Create combined start script
    combined_script = Path("start_both.py")
    combined_script.write_text("""#!/usr/bin/env python3
import os
import subprocess
import sys
import threading
import time

def start_agent():
    print("🤖 Starting agent...")
    os.chdir("agent-starter-python")
    subprocess.run(["python", "deploy.py", "local"])

def start_frontend():
    print("🌐 Starting frontend...")
    time.sleep(3)  # Give agent time to start
    os.chdir("../agent-starter-react")
    subprocess.run(["pnpm", "dev"])

def main():
    print("🚀 Starting LiveKit Agent + Frontend")
    print("=" * 40)
    
    try:
        # Start agent in background thread
        agent_thread = threading.Thread(target=start_agent, daemon=True)
        agent_thread.start()
        
        # Start frontend in main thread
        start_frontend()
        
    except KeyboardInterrupt:
        print("\\n🛑 Stopping all services...")

if __name__ == "__main__":
    main()
""")
    combined_script.chmod(0o755)
    
    print("✅ Startup scripts created:")
    print("  • start_agent.py - Start just the agent")
    print("  • start_frontend.py - Start just the frontend")
    print("  • start_both.py - Start both together")

def main():
    """Main setup process"""
    print("🎯 LiveKit Frontend Integration Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix the issues above.")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed.")
        sys.exit(1)
    
    # Create startup scripts
    create_startup_scripts()
    
    print("\n🎉 Frontend setup complete!")
    print("\n📋 Next steps:")
    print("  1. Start the agent: python start_agent.py")
    print("  2. In another terminal, start frontend: python start_frontend.py")
    print("  3. Or start both together: python start_both.py")
    print("  4. Open http://localhost:3000 in your browser")
    print("\n💡 Tips:")
    print("  • Make sure you have valid API keys configured")
    print("  • The agent must be running before connecting from frontend")
    print("  • Check browser console for any connection issues")

if __name__ == "__main__":
    main()
