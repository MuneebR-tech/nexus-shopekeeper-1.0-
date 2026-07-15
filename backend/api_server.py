"""
Nexus Shopkeeper - Phase 2 API Server
Launches the FastAPI server, enables CORS, includes the router endpoints,
and mounts/serves the frontend static files.
"""

import sys
import os
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

# Force UTF-8 encoding for standard streams on Windows to prevent print/logging crashes
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Add project root to python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Load .env file configurations
load_dotenv(PROJECT_ROOT / ".env")

from backend.api.router import router as api_router

app = FastAPI(
    title="Nexus Shopkeeper API Server",
    description="Commercial Retail SaaS Backend with K-Means clustering and Reactive Store Credit Engine.",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix="/api")

# Redirect root and clean paths to the static HTML templates
@app.get("/")
def redirect_to_portal():
    return RedirectResponse(url="/templates/index.html")

@app.get("/index")
def redirect_clean_portal():
    return RedirectResponse(url="/templates/index.html")

@app.get("/kiosk")
def redirect_clean_kiosk():
    return RedirectResponse(url="/templates/kiosk.html")

@app.get("/dashboard")
def redirect_clean_dashboard():
    return RedirectResponse(url="/templates/dashboard.html")

@app.get("/phase1")
def redirect_clean_phase1():
    return RedirectResponse(url="/templates/phase1.html")

# Mount frontend directory for static serving
frontend_path = PROJECT_ROOT / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")
else:
    print(f"  ⚠ Warning: Frontend folder not found at {frontend_path}. Kiosk GUI will not be accessible.")


def main():
    port = int(os.getenv("PORT", 8000))
    print("========================================================================")
    print("  NEXUS SHOPKEEPER - Phase 2 FastAPI Server Boot")
    print(f"  Local URL: http://localhost:{port}")
    print(f"  API Docs:  http://localhost:{port}/docs")
    print("========================================================================")
    
    # Run uvicorn on configured port
    uvicorn.run(app, host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
