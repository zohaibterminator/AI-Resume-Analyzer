from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


class User(BaseModel):
    name: str
    email_id: EmailStr
    mobile_num: str


class Resume(BaseModel):
    resume_score: float
    no_of_pages: int
    timestamp: datetime
    user_level: str
    skills: List
    total_experience: float
    job_description: str