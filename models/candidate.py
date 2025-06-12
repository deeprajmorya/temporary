from dataclasses import dataclass
from typing import List, Optional
from datetime import date

@dataclass
class Candidate:
    """
    Represents a candidate's resume with structured data
    """
    id: str  # Unique identifier (can be file hash)
    raw_text: str  # Original extracted text
    name: Optional[str] = None
    skills: List[str] = None
    experiences: List['Experience'] = None
    education: List['Education'] = None
    file_path: Optional[str] = None  # Where the resume is stored

    def __post_init__(self):
        """Basic validation"""
        if not self.raw_text:
            raise ValueError("Candidate must have raw_text")
        self.skills = self.skills or []
        self.experiences = self.experiences or []
        self.education = self.education or []

@dataclass
class Experience:
    title: str
    company: str
    start_date: date
    end_date: Optional[date]  # None for current positions
    description: str

@dataclass
class Education:
    degree: str
    institution: str
    year_completed: int