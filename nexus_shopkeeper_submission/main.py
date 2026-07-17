"""
Nexus Shopkeeper - Master Root Entry Point (`main.py`)
Allows running the entire application directly from the root directory (`python main.py`).
Provides full compatibility for automated evaluation scripts and instructor testing.
"""
import sys
import os
import uvicorn
from pathlib import Path

# Ensure project root is at the top of sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import the core FastAPI application and launcher from the backend
from backend.api_server import app, main as server_main

if __name__ == "__main__":
    print("========================================================================")
    print("  NEXUS SHOPKEEPER - Root Entry Point Launch (`main.py`)")
    print("========================================================================")
    server_main()
