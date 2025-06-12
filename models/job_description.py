from dataclasses import dataclass
from typing import List, Optional

@dataclass
class JobDescription:
    """
    Structured representation of a job posting
    """
    id: str  # Can be file hash or UUID
    raw_text: str
    job_title: Optional[str] = None
    required_skills: List[str] = None
    preferred_skills: List[str] = None
    min_experience: Optional[int] = None  # In years
    education_requirements: Optional[str] = None
    file_path: Optional[str] = None

    def __post_init__(self):
        """Normalize data"""
        if not self.raw_text:
            raise ValueError("JobDescription must have raw_text")
        self.required_skills = self.required_skills or []
        self.preferred_skills = self.preferred_skills or []