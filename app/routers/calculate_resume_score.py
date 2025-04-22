from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from routers.schemas.models import Resume
from db.database import get_db
from db import models
from db.utils import get_gemini_client


router = APIRouter()

@router.post("/")
async def calculate_resume_score(resume: Resume, user_id: int, db: Session = Depends(get_db)):
    print
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        client = get_gemini_client()

        resume_text = f"""
        Name: {user.name}
        Resume Score: {resume.resume_score}
        No. Of Pages: {resume.no_of_pages}
        Skills: {', '.join(resume.skills)}
        Experience: {resume.total_experience}
        Level: {resume.user_level}
        """

        prompt = f"""
            You are an experienced HR Manager with Technical Experience in the field of any one job role from Data Science, Data Analyst, DevOPS, Machine Learning Engineer, Prompt Engineer, AI Engineer, Full Stack Web Development, Big Data Engineering, Marketing Analyst, Human Resource Manager, Software Developer, etc. Your task is to review the provided resume and rate whether the candidate is a good match for the provided Job Description. As your response, ONLY give a single number out of 100 as a rating for the resume. Don't give any other explanation or details. Just give the number.

            Resume: {resume_text}
            Job Description: {resume.job_description}
        """

        resume_score = client.generate_content(
            prompt
        )

        return {
            "resume_score": resume_score.text,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))