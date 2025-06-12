from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Optional
from utils.storage import StorageManager
from utils.validations import InputValidator
from services.parser import FileParser
from routes. global_store import parsed_jd_store, parsed_candidates_store
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_files(
    jd_file: Optional[UploadFile] = File(None),
    jd_text: Optional[str] = Form(None),
    resumes: Optional[List[UploadFile]] = File(None)
):
    # Validate presence of JD input
    is_jd_valid, jd_error = InputValidator.validate_jd_input(jd_text, jd_file)
    if not is_jd_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=jd_error)

    # Validate presence of resumes
    is_resume_valid, resume_error = InputValidator.validate_resumes(resumes)
    if not is_resume_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=resume_error)

    jd_obj = None
    # Save JD if it's a file
    if jd_file:
        success, path_or_err = StorageManager.save_upload(jd_file, upload_type="job_description")
        if not success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=path_or_err)
        jd_obj = FileParser.parse_to_jd(path_or_err)
    else:
        # Save from text
        jd_obj = FileParser.parse_to_jd_from_text(jd_text)

    # Assign a unique ID to JD and store it
    jd_id = uuid.uuid4().hex
    jd_obj.id = jd_id
    parsed_jd_store[jd_id] = jd_obj

    candidate_ids = []

    for resume in resumes:
        success, path_or_err = StorageManager.save_upload(resume, upload_type="resume")
        if not success:
            continue  # skip invalid resume

        candidate_obj = FileParser.parse_to_candidate(path_or_err)
        candidate_id = uuid.uuid4().hex
        candidate_obj.id = candidate_id
        parsed_candidates_store[candidate_id] = candidate_obj
        candidate_ids.append(candidate_id)

    if len(candidate_ids) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All resume uploads failed.")

    return JSONResponse(status_code=200, content={
        "message": "Upload successful.",
        "job_description_id": jd_id,
        "candidate_ids": candidate_ids
    })
