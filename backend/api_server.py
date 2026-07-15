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
from fastapi.responses import RedirectResponse, HTMLResponse
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

# Locate frontend directory across multiple possible root locations
possible_roots = [
    PROJECT_ROOT / "frontend",
    Path.cwd() / "frontend",
    Path(__file__).resolve().parent / "frontend"
]
frontend_path = None
for p in possible_roots:
    if p.exists():
        frontend_path = p
        break

def get_missing_folder_html():
    return HTMLResponse(
        content="""
        <html>
        <head><title>Nexus Shopkeeper - Extraction Required</title></head>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #ffffff; padding: 40px; text-align: center;">
            <div style="max-width: 650px; margin: 50px auto; background: #1e1e1e; padding: 35px; border-radius: 12px; border: 2px solid #ff4444; box-shadow: 0 8px 24px rgba(255,68,68,0.2);">
                <h1 style="color: #ff4444; margin-bottom: 10px;">⚠️ Project Not Fully Extracted</h1>
                <p style="font-size: 18px; line-height: 1.6; color: #dddddd;">
                    The web server started, but could not find the <code>frontend</code> HTML templates folder.
                </p>
                <div style="font-size: 16px; background: #2a2a2a; padding: 20px; border-radius: 8px; text-align: left; margin: 25px 0; border-left: 4px solid #ffbb33;">
                    <strong style="color: #ffbb33;">Why did this happen?</strong><br>
                    You likely double-clicked <code>start_app.bat</code> directly inside the Windows compressed ZIP folder view without extracting all the folders first.
                </div>
                <div style="font-size: 16px; background: #1b3320; padding: 20px; border-radius: 8px; text-align: left; border-left: 4px solid #00C851;">
                    <strong style="color: #00C851;">How to fix it immediately:</strong><br>
                    <ol style="margin-top: 10px; margin-bottom: 0; padding-left: 20px; line-height: 1.8;">
                        <li>Close this browser window and the black server terminal window.</li>
                        <li>Right-click the <code>nexus_shopkeeper_submission.zip</code> file and select <strong>Extract All...</strong></li>
                        <li>Open the newly extracted folder and run <code>start_app.bat</code> from inside it!</li>
                    </ol>
                </div>
            </div>
        </body>
        </html>
        """,
        status_code=404
    )

if frontend_path:
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
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="static")
else:
    print(f"  ⚠ Warning: Frontend folder not found at {PROJECT_ROOT / 'frontend'}. Serving extraction guide.")
    @app.get("/")
    def serve_missing_root():
        return get_missing_folder_html()

    @app.get("/{path:path}")
    def serve_missing_catchall(path: str):
        return get_missing_folder_html()


def main():
    initial_port = int(os.getenv("PORT", 8000))
    candidate_ports = [initial_port, 8001, 8002, 8080, 8888, 5000, 5001]
    
    # Remove duplicates while preserving order
    ports_to_try = []
    for p in candidate_ports:
        if p not in ports_to_try:
            ports_to_try.append(p)
            
    import socket
    selected_port = initial_port
    for p in ports_to_try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", p))
                selected_port = p
                break
            except OSError:
                print(f"  [!] Port {p} is currently in use. Trying next available port...")
                continue
                
    # Save active port for launcher verification
    try:
        data_dir = PROJECT_ROOT / "data"
        data_dir.mkdir(exist_ok=True)
        with open(data_dir / "active_port.txt", "w", encoding="utf-8") as pf:
            pf.write(str(selected_port))
    except Exception as e:
        print(f"  [!] Could not write active_port.txt: {e}")

    print("========================================================================")
    print("  NEXUS SHOPKEEPER - Phase 2 FastAPI Server Boot")
    print(f"  Local URL: http://localhost:{selected_port}")
    print(f"  API Docs:  http://localhost:{selected_port}/docs")
    print("========================================================================")
    
    # Run uvicorn on verified available port
    uvicorn.run(app, host="127.0.0.1", port=selected_port)


if __name__ == "__main__":
    main()
