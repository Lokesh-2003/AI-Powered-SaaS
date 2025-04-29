from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResumeBase(BaseModel):
    filename: str
    filepath: str

class ResumeCreate(ResumeBase):
    user_id: int

class Resume(ResumeBase):
    id: int
    user_id: int
    upload_date: datetime
    analysis_result: Optional[str] = None
    status: str

    class Config:
        orm_mode = True