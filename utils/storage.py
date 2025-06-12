import os
from pathlib import Path
from werkzeug.utils import secure_filename
from config import Config
from typing import Tuple
import uuid

class StorageManager:
    @staticmethod
    def save_upload(file, upload_type: str) -> Tuple[bool, str]:
        """
        Saves uploaded file with secure random filename
        Args:
            file: Werkzeug FileStorage object
            upload_type: 'resume' or 'job_description'
        Returns:
            Tuple[success: bool, saved_path_or_error: str]
        """
        try:
            # Validate input
            if not file or file.filename == '':
                return False, "No selected file"
            
            # Generate secure filename
            file_ext = os.path.splitext(file.filename)[1].lower()
            if file_ext not in Config.ALLOWED_EXTENSIONS:
                return False, f"Invalid file type. Allowed: {Config.ALLOWED_EXTENSIONS}"
            
            random_id = uuid.uuid4().hex
            safe_filename = f"{random_id}{file_ext}"
            
            # Determine save directory
            save_dir = Config.RESUME_DIR if upload_type == 'resume' else Config.JD_DIR
            save_path = os.path.join(save_dir, safe_filename)
            
            # Save file
            file.save(save_path)
            return True, save_path
            
        except Exception as e:
            return False, f"Storage error: {str(e)}"

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Safely removes a stored file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception:
            return False