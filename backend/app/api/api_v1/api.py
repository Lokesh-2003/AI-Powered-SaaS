from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Resume Analyzer API"}