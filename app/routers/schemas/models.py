from pydantic import BaseModel, EmailStr
from typing import List


class Use(BaseModel):
    name: str
    email: EmailStr
    mobile_num: str


class Resume(BaseModel):
    resume_score: float
    no_of_pages: int
    user_level: str
    skills: List
    total_experience: float