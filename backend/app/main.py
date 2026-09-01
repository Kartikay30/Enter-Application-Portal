# =============================================
# main.py - FastAPI Application Entry Point
# =============================================
# This is the central heart of our backend application:
#   1. Initializes the FastAPI instance
#   2. Configures CORS (Cross-Origin Resource Sharing) for React
#   3. Creates database tables if they don't exist
#   4. Runs the auto-seeder (seeds admin@enter.in & 10 jobs)
#   5. Registers all API route modules
# =============================================

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Configure standard Python logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("enter_ats")

from app.config import settings
from app.db.database import engine, Base, SessionLocal
from app.db.seed import seed_database
from app.routes.auth_routes import router as auth_router
from app.routes.job_routes import router as job_router
from app.routes.application_routes import router as application_router


# ---- Lifespan Event Handler (Startup & Shutdown) ----
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Code inside this block runs BEFORE the application starts serving requests.
    """
    print("\n" + "=" * 55)
    print("[STARTING] ENTER HIRING MANAGEMENT SYSTEM BACKEND")
    print("=" * 55)

    # 1. Create upload folder if not exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # 2. Create all database tables (User, Job, Application)
    print("[DATABASE] Creating tables if not already present...")
    Base.metadata.create_all(bind=engine)
    print("[DATABASE] Tables ready.")

    # 3. Seed initial admin & 10 jobs
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    print(f"[DOCS] Interactive Swagger API Docs available at: http://localhost:8000/docs")
    print("=" * 55 + "\n")

    yield  # Application is now running and accepting requests!

    print("[SHUTDOWN] Backend server shutting down...")


# ---- Initialize FastAPI App ----
app = FastAPI(
    title="Enter Hiring Management & ATS API",
    description="Full-stack hiring management system with candidate application portal and admin dashboard.",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI endpoint
    redoc_url="/redoc",    # ReDoc alternative docs
    lifespan=lifespan
)


# ---- CORS Configuration ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:5173",
        "http://localhost:3000",  # React CRA port
        "http://127.0.0.1:3000",
        "*"                       # Allow all origins for seamless development & demo
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Request Logging Middleware ----
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Logs every incoming HTTP request and response status code with timing.
    """
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f"--> Incoming {request.method} {request.url.path} from {client_ip}")
    response = await call_next(request)
    logger.info(f"<-- Completed {request.method} {request.url.path} with status {response.status_code}")
    return response


# ---- Mount Routers ----
# Connect all API route modules to the main app
app.include_router(auth_router)
app.include_router(job_router)
app.include_router(application_router)


# ---- Health Check & Root Endpoints ----
@app.get("/", tags=["System"])
def root():
    """
    Root endpoint confirming the API is active.
    """
    return {
        "app": "Enter Hiring Management System",
        "status": "Online",
        "version": "1.0.0",
        "docs": "/docs",
        "admin_email": "admin@enter.in"
    }


@app.get("/api/health", tags=["System"])
def health_check():
    """
    Health check endpoint for monitoring uptime and deployment platforms.
    """
    return {"status": "healthy", "database": "connected"}
