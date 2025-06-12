import os
import PyPDF2
from docx import Document
from pathlib import Path
from typing import Union
from models import Candidate, JobDescription

class FileParser:
    @staticmethod
    def parse_to_candidate(file_path: str) -> Candidate:
        """Converts resume file to structured Candidate"""
        text = FileParser._extract_text(file_path)
        return Candidate(
            id=os.path.basename(file_path),
            raw_text=text,
            file_path=file_path
        )

    @staticmethod
    def parse_to_jd(file_path: str) -> JobDescription:
        """Converts JD file to structured JobDescription"""
        text = FileParser._extract_text(file_path)
        return JobDescription(
            id=os.path.basename(file_path),
            raw_text=text,
            file_path=file_path
        )

    @staticmethod
    def _extract_text(file_path: Union[str, Path]) -> str:
        """Universal text extractor for supported formats"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return '\n'.join(page.extract_text() for page in reader.pages)
                
        elif file_ext == '.docx':
            return '\n'.join(
                p.text for p in Document(file_path).paragraphs
            )
            
        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        raise ValueError(f"Unsupported file type: {file_ext}")