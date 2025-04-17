from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List


class Skill(BaseModel):
    skill_name: str
    type: str  # "Actual" or "Recommended"


class UserAttributes(BaseModel):
    predicted_field: str
    user_level: str


class Resume(BaseModel):
    name: str
    email: EmailStr
    resume_score: float
    timestamp: datetime
    page_no: int
    predicted_field: str
    user_level: str
    actual_skills: List[str]
    recommended_skills: List[str]