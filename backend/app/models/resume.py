from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    filepath = Column(String)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    analysis_result = Column(Text, nullable=True)
    status = Column(String, default="pending")  # pending, processing, completed, failed