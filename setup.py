#!/usr/bin/env python3
"""Setup script for ToneShift AI."""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🎭 ToneShift AI Setup")
    print("=" * 50)
    
    # Check if uv is installed
    if not run_command("uv --version", "Checking uv installation"):
        print("\n❌ uv is not installed. Please install it first:")
        print("curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("Or visit: https://docs.astral.sh/uv/getting-started/installation/")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("uv sync", "Installing dependencies"):
        print("\n❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists():
        if Path("env.example").exists():
            run_command("cp env.example .env", "Creating .env file")
        else:
            print("⚠️  No env.example file found, creating basic .env")
            with open(".env", "w") as f:
                f.write("DEBUG=True\nHOST=0.0.0.0\nPORT=8000\n")
    
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 To start the application, run:")
    print("   uv run python run.py")
    print("\n🌐 Then open your browser to:")
    print("   http://localhost:8000")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()
