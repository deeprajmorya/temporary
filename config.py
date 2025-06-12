import os
from pathlib import Path

class Config:
    # File Storage Settings
    BASE_DIR = Path(__file__).parent.parent
    STORAGE_DIR = BASE_DIR / "storage"
    RESUME_DIR = STORAGE_DIR / "resumes"
    JD_DIR = STORAGE_DIR / "job_description"
    
    # Create directories if they don't exist
    for dir_path in [STORAGE_DIR, RESUME_DIR, JD_DIR]:
        dir_path.mkdir(exist_ok=True)
    
    # Gemini Settings
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Set this in your environment
    MODEL_NAME = "gemini-1.5-flash"
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}