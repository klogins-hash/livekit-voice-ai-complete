#!/usr/bin/env python3
"""
Deployment helper script for LiveKit Agent Starter
Supports Docker deployment and basic production setup.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def check_docker():
    """Check if Docker is available"""
    try:
        run_command("docker --version")
        return True
    except:
        return False

def check_env_file():
    """Check if .env.local is properly configured"""
    env_file = Path(".env.local")
    if not env_file.exists():
        return False, ".env.local file not found"
    
    content = env_file.read_text()
    if "your_" in content:
        return False, "Placeholder values found in .env.local"
    
    return True, "Environment file configured"

def build_docker_image(tag="livekit-agent"):
    """Build Docker image"""
    print(f"🐳 Building Docker image: {tag}")
    run_command(f"docker build -t {tag} .")
    print(f"✅ Docker image built: {tag}")

def run_docker_container(tag="livekit-agent", detached=True):
    """Run Docker container"""
    env_file = Path(".env.local")
    if not env_file.exists():
        print("❌ .env.local file not found. Run configure_env.py first.")
        sys.exit(1)
    
    detach_flag = "-d" if detached else ""
    print(f"🚀 Running Docker container: {tag}")
    
    cmd = f"docker run {detach_flag} --env-file .env.local --name livekit-agent-instance {tag}"
    
    if detached:
        container_id = run_command(cmd)
        print(f"✅ Container started: {container_id[:12]}")
        print("📋 Useful commands:")
        print(f"  • View logs: docker logs -f {container_id[:12]}")
        print(f"  • Stop container: docker stop {container_id[:12]}")
        print(f"  • Remove container: docker rm {container_id[:12]}")
    else:
        os.system(cmd)

def deploy_local():
    """Deploy locally using uv"""
    print("🏠 Starting local deployment...")
    
    # Check environment
    env_ok, env_msg = check_env_file()
    if not env_ok:
        print(f"❌ Environment check failed: {env_msg}")
        print("Run: uv run python configure_env.py")
        sys.exit(1)
    
    print("✅ Environment configured")
    
    # Run setup check
    print("🔍 Running setup verification...")
    result = subprocess.run(["uv", "run", "python", "setup_check.py"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Setup verification failed:")
        print(result.stdout)
        sys.exit(1)
    
    print("✅ Setup verification passed")
    
    # Start the agent
    print("🚀 Starting LiveKit agent...")
    print("Press Ctrl+C to stop")
    
    try:
        subprocess.run(["uv", "run", "python", "src/agent.py", "start"])
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped")

def main():
    parser = argparse.ArgumentParser(description="Deploy LiveKit Agent")
    parser.add_argument(
        "mode", 
        choices=["docker", "local", "build"], 
        help="Deployment mode"
    )
    parser.add_argument(
        "--tag", 
        default="livekit-agent", 
        help="Docker image tag (for docker mode)"
    )
    parser.add_argument(
        "--interactive", 
        action="store_true", 
        help="Run Docker container interactively"
    )
    
    args = parser.parse_args()
    
    print("🚀 LiveKit Agent Deployment")
    print("=" * 30)
    
    if args.mode == "build":
        if not check_docker():
            print("❌ Docker not found. Please install Docker first.")
            sys.exit(1)
        build_docker_image(args.tag)
    
    elif args.mode == "docker":
        if not check_docker():
            print("❌ Docker not found. Please install Docker first.")
            sys.exit(1)
        
        # Build if image doesn't exist
        try:
            run_command(f"docker image inspect {args.tag}")
        except:
            print(f"🔨 Image {args.tag} not found, building...")
            build_docker_image(args.tag)
        
        run_docker_container(args.tag, not args.interactive)
    
    elif args.mode == "local":
        deploy_local()

if __name__ == "__main__":
    main()
