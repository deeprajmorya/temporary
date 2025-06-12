import re
from typing import List, Optional
from models import Candidate, JobDescription
from .gemini_client import GeminiClient


class ResumeMatcher:
    def __init__(self):
        self.gemini = GeminiClient()

    def rank_candidates(
        self,
        candidates: List[Candidate],
        jd: JobDescription
    ) -> List[dict]:
        """
        Ranks candidates based on Gemini's AI score (1–100).
        Returns a list of dicts with candidate info, AI score, fit category, and analysis.
        """
        results = []

        for candidate in candidates:
            ai_analysis = self.gemini.generate_match_report(candidate, jd)
            if not ai_analysis:
                continue  # skip candidate if analysis failed

            ai_score, fit_category = self._extract_score_and_fit(ai_analysis)

            if ai_score is None:
                continue  # skip malformed response

            results.append({
                "candidate_id": candidate.id,
                "file_path": candidate.file_path,
                "ai_score": ai_score,
                "fit": fit_category,
                "ai_analysis": ai_analysis
            })

        return sorted(results, key=lambda x: x["ai_score"], reverse=True)

    def _extract_score_and_fit(self, analysis_text: str) -> tuple[Optional[int], Optional[str]]:
        """
        Extracts the AI-generated integer score and fit category from Gemini markdown output.
        Expected format in output:
        **Rating**: 85  
        **Fit**: Good Fit
        """
        score_match = re.search(r"\*\*Rating\*\*:\s*(\d{1,3})", analysis_text)
        fit_match = re.search(r"\*\*Fit\*\*:\s*(Poor Fit|Average Fit|Good Fit)", analysis_text, re.IGNORECASE)

        try:
            score = int(score_match.group(1)) if score_match else None
            if score is not None and (score < 1 or score > 100):
                score = None
        except ValueError:
            score = None

        fit = fit_match.group(1).title() if fit_match else None

        return score, fit
