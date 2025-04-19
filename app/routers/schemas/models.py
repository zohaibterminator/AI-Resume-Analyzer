from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


class User(BaseModel):
    name: str
    email: EmailStr
    mobile_num: str


class Resume(BaseModel):
    resume_score: float
    timestamp: datetime
    no_of_pages: int
    user_level: str
    skills: List
    total_experience: float
    job_description: str