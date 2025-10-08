#!/usr/bin/env python3
"""Startup script for ToneShift AI application."""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5173))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print("🎭 Starting ToneShift AI...")
    print(f"📍 Server: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print("🚀 Loading models... (this may take a moment)")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if debug else "warning"
    )
