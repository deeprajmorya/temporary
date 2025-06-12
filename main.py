# main.py

import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routes import uploads, matching
from config import Config  # assuming your config.py has class Config
LOG_DIR = "logs"
LOG_FILE = "app.log"

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/{LOG_FILE}"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("resume_matcher_app")

# Setup logger
logger = logging.getLogger("resume_ranker")
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(" Starting up AI Resume Ranker API...")
    try:
        # You could init embeddings, Gemini, DB etc. here
        logger.info(" Services initialized.")
        yield
    finally:
        logger.info(" Shutting down AI Resume Ranker API...")


app = FastAPI(
    title="AI Resume Ranker",
    description="Upload resumes and a job description to get ranked candidates using Gemini AI.",
    version="1.0.0",
    docs_url=None,  # Swagger UI disabled
    redoc_url=None,  # Redoc disabled
    lifespan=lifespan
)

# CORS (allow all for now — restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Route registration
app.include_router(uploads.router, prefix="/v1")
app.include_router(matching.router, prefix="/v1")


@app.get("/health")
async def health():
    logger.info("Health check requested.")
    return {
        "status": "ready",
        "services": ["upload", "matcher", "gemini"]
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Running app on localhost:8000")
    uvicorn.run(
        "main:app",  # Required for hot reload
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )
