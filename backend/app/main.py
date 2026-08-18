import logging
import os
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import ValidationError

from .routes import blockchain_router, transaction_router
from core.exceptions import BlockchainException

# ============================================================================
# Logging Configuration
# ============================================================================
def setup_logging():
    """Configure logging for the application."""
    log_dir = Path(__file__).resolve().parents[2] / "logs"
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"blockchain_app_{timestamp}.log"
    
    # Configure logging with both console and file handlers
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()

# ============================================================================
# FastAPI App Setup
# ============================================================================
app = FastAPI(
    title="Mini Blockchain Visualizer",
    description="A compact blockchain explorer with Merkle tree visualization and tampering detection.",
    version="1.0.0",
)

# ============================================================================
# Middleware Setup
# ============================================================================
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "mini-merkle-blockchain-demo-secret-key"),
    same_site="lax",
    https_only=os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true",
)

# CORS Middleware - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Request/Response Logging Middleware
# ============================================================================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and outgoing responses."""
    logger.info(f"→ {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        logger.info(f"← {request.method} {request.url.path} - {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"✗ {request.method} {request.url.path} - Exception: {str(e)}", exc_info=True)
        raise

# ============================================================================
# Exception Handlers
# ============================================================================
@app.exception_handler(BlockchainException)
async def blockchain_exception_handler(request: Request, exc: BlockchainException):
    """Handle custom blockchain exceptions."""
    logger.error(f"Blockchain error on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc), "type": exc.__class__.__name__},
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors."""
    logger.warning(f"Validation error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Invalid request data", "errors": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"},
    )

# ============================================================================
# Frontend Setup
# ============================================================================
frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
static_dir = frontend_dir / "static"

if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", tags=["Root"])
async def root():
    """Serve the frontend index.html."""
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Mini Blockchain Visualizer - Backend is running"}

# ============================================================================
# Route Registration
# ============================================================================
app.include_router(blockchain_router.router)
app.include_router(transaction_router.router)

logger.info("Mini Blockchain Visualizer backend initialized successfully")