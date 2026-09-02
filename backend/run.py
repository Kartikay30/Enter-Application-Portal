# =============================================
# run.py - Startup Script
# =============================================
# This file is the ENTRY POINT to start the backend server.
# Just run: python run.py
#
# Locally:  Runs on http://localhost:8000 with auto-reload
# Railway:  Reads PORT from environment variable (e.g., PORT=3000)
# =============================================

import os
import uvicorn  # Uvicorn is the server that runs FastAPI

if __name__ == "__main__":
    # Railway sets PORT as an environment variable.
    # Locally we default to 8000.
    port = int(os.environ.get("PORT", 8000))

    # In production (Railway), disable reload for stability.
    # Locally, enable reload for developer convenience.
    is_production = os.environ.get("RAILWAY_ENVIRONMENT") is not None

    print(f"[SERVER] Starting on port {port} (production={is_production})")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",          # Accept connections from any IP
        port=port,               # Use Railway's PORT or default 8000
        reload=not is_production # Auto-reload only in development
    )

