#!/usr/bin/env python3
"""
Development server startup script.

Usage:
    python run.py                    # Start on localhost:8000
    python run.py --reload          # Enable auto-reload
    python run.py --port 8001       # Custom port
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    import uvicorn

    # Parse optional arguments
    args = sys.argv[1:]
    reload = "--reload" in args
    port = 8000

    for i, arg in enumerate(args):
        if arg == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
            args.pop(i + 1)
            args.pop(i)
            break

    print(f"Starting Deepfake Video Detection API...")
    print(f"Host: 127.0.0.1")
    print(f"Port: {port}")
    print(f"Reload: {reload}")
    print(f"Docs: http://127.0.0.1:{port}/docs")

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=port,
        reload=reload,
    )
