import re
from typing import Optional, Tuple

class InputValidator:
    @staticmethod
    def validate_jd_input(jd_text: Optional[str], jd_file) -> Tuple[bool, str]:
        """
        Validates either text or file JD input
        Returns:
            Tuple[is_valid: bool, error_message: str]
        """
        if not jd_text and not jd_file:
            return False, "Either text or file must be provided"
        
        if jd_text and len(jd_text.strip()) < 50:
            return False, "Job description too short (min 50 chars)"
        
        return True, ""

    @staticmethod
    def validate_resumes(resume_files) -> Tuple[bool, str]:
        if not resume_files or len(resume_files) == 0:
            return False, "At least one resume required"
        
        if len(resume_files) > 10:
            return False, "Maximum 10 resumes allowed"
        
        return True, ""

    @staticmethod
    def sanitize_text(input_text: str) -> str:
        """Basic sanitization for user-provided text"""
        return re.sub(r'[^\w\s.,-]', '', input_text).strip()