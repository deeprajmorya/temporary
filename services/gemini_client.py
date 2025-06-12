import google.generativeai as genai
from config import Config
from typing import Optional
from models import Candidate, JobDescription

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL_NAME)
        self.safety_settings = {
            'HARASSMENT': 'BLOCK_NONE',
            'HATE': 'BLOCK_NONE',
            'SEXUAL': 'BLOCK_NONE',
            'DANGEROUS': 'BLOCK_NONE'
        }

    def generate_match_report(
        self,
        candidate: Candidate,
        jd: JobDescription
    ) -> Optional[str]:
        """
        Generates detailed match analysis with:
        - Skill matches
        - Experience evaluation
        - Education alignment
        - Overall fit reasoning
        - Integer rating from 1 to 100
        - Fit category (Poor Fit / Average Fit / Good Fit)
        """
        prompt = f"""**Resume Matching Analysis**

            Evaluate the candidate profile against the job description.

            **Job Description**:
            {jd.raw_text[:3000]}... (truncated)

            **Candidate Resume**:
            {candidate.raw_text[:3000]}... (truncated)

            Provide a markdown report with these sections:

            ### 1. Top 3 Skill Matches  
            Highlight and explain the top 3 matching skills.

            ### 2. Experience Comparison  
            Summarize how the candidate's experience aligns with the job’s required experience (industry, years, relevance).

            ### 3. Education Verification  
            Check if the candidate’s education meets the minimum qualification and comment on alignment.

            ### 4. Final Verdict  
            Provide:
            - A **rating**: integer between 1 and 100 (no decimal)
            - A **fit category**: choose one of **Poor Fit**, **Average Fit**, or **Good Fit**
            - A short **justification** (2–3 lines)

            **Format Example**:
            **Rating**: 85  
            **Fit**: Good Fit  
            **Justification**: Strong match on skills and experience; education also meets requirements.
            """

        try:
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            print(f"Gemini error: {str(e)}")
            return None
