from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from routes.global_store import parsed_jd_store, parsed_candidates_store
from services.matcher import ResumeMatcher

router = APIRouter()

@router.post("/match")
def match_resumes(job_description_id: str):
    if job_description_id not in parsed_jd_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job Description not found")

    jd = parsed_jd_store[job_description_id]
    candidates = list(parsed_candidates_store.values())

    if not candidates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No resumes uploaded")

    matcher = ResumeMatcher()
    ranked_results = matcher.rank_candidates(candidates, jd)

    if not ranked_results:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="AI analysis failed for all candidates")

    return JSONResponse(status_code=200, content={
        "job_description_id": job_description_id,
        "top_matches": ranked_results[:3]  # return top 3 matches
    })
