"""
Nexus Shopkeeper - Application Entry Point (`app.py`)
Provides direct compatibility for automated grading scripts, cloud deployment portals, and instructor evaluation.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.api_server import app, main

if __name__ == "__main__":
    print("========================================================================")
    print("  NEXUS SHOPKEEPER - Application Entry Point (`app.py`)")
    print("========================================================================")
    main()
