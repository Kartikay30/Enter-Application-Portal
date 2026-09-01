# =============================================
# run.py - Startup Script
# =============================================
# This file is the ENTRY POINT to start the backend server.
# Just run: python run.py
# It will start the FastAPI server on http://localhost:8000
# =============================================

import uvicorn  # Uvicorn is the server that runs FastAPI

if __name__ == "__main__":
    # Start the server with these settings:
    # - "app.main:app" means -> go to app/main.py and find the 'app' object
    # - host="0.0.0.0" means -> accept connections from any IP (not just localhost)
    # - port=8000 means -> run on port 8000 (http://localhost:8000)
    # - reload=True means -> auto-restart when you save code changes (great for development!)
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
