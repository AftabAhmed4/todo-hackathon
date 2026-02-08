"""
FastAPI application entry point.

Main application configuration including CORS middleware.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import time
import logging
from db import create_db_and_tables
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Get frontend URL from environment
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Create FastAPI app
app = FastAPI(
    title="Todo App API",
    description="Authentication API for Todo Web Application",
    version="1.0.0"
)

print(f"Frontend URL for CORS: {FRONTEND_URL}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
)


# Request/Response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and outgoing responses."""
    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Log response
    process_time = time.time() - start_time
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Duration: {process_time:.3f}s"
    )

    return response


@app.on_event("startup")
def on_startup():
    """Create database tables on startup and validate environment."""
    # Validate required environment variables
    required_env_vars = ["DATABASE_URL", "BETTER_AUTH_SECRET"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]

    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    logger.info("Environment variables validated successfully")
    logger.info("Creating database tables...")
    create_db_and_tables()
    logger.info("Database tables created successfully")


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Todo App API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include authentication routes
from routes.auth import router as auth_router
app.include_router(auth_router)

# Include task routes
from routes.tasks import router as tasks_router
app.include_router(tasks_router)

# Include chat routes
from routes.chat import router as chat_router
app.include_router(chat_router)
