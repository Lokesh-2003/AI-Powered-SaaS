import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.db.dependencies import get_db
from app.schemas.resume import Resume, ResumeCreate
from app.services.resume import (
    get_resume,
    get_resumes_by_user,
    create_user_resume,
    update_resume_analysis,
)
from app.services.user import get_current_user
from app.ml_model.resume_parser import parse_resume
from app.core.config import settings

router = APIRouter()

@router.post("/upload", response_model=Resume)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Save file to uploads directory
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    # Create resume record in database
    resume_data = ResumeCreate(
        filename=file.filename,
        filepath=file_path,
        user_id=current_user.id
    )
    db_resume = create_user_resume(db=db, resume=resume_data)
    
    # Process resume in background (in a real app, use Celery or similar)
    try:
        analysis_result = parse_resume(file_path)
        update_resume_analysis(
            db=db, 
            resume_id=db_resume.id, 
            analysis_result=analysis_result,
            status="completed"
        )
    except Exception as e:
        update_resume_analysis(
            db=db, 
            resume_id=db_resume.id, 
            analysis_result=str(e),
            status="failed"
        )
        raise HTTPException(status_code=500, detail=str(e))
    
    return db_resume

@router.get("/{resume_id}", response_model=Resume)
def read_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_resume = get_resume(db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    if db_resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this resume")
    return db_resume

@router.get("/", response_model=List[Resume])
def read_user_resumes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resumes = get_resumes_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return resumes