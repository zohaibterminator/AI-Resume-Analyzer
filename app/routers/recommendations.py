from fastapi import APIRouter, HTTPException, Depends
import google.generativeai as genai
from sqlalchemy.orm import Session
from routers.schemas.models import Resume
from db.database import get_db
from db import models
import os
from dotenv import load_dotenv


def get_gemini_client():
    return genai.GenerativeModel(
        model_name="gemini-2.0-pro",
        api_key=os.getenv("GOOGLE_API_KEY")
    )


router = APIRouter()

@router.post("/")
async def generate_recommendations(resume: Resume, user_id: int, db: Session = Depends(get_db)):
    try:
        client = get_gemini_client()

        resume_text = f"""
        Name: {resume.name}
        Email: {resume.email}
        Skills: {', '.join(resume.skills)}
        Experience: {resume.experience}
        Education: {resume.education}
        Certifications: {resume.certifications}
        """

        prompt = f"""
        You are an experienced HR with Technical Experience in the field of any one job role from Data Science, Data Analyst, DevOPS, Machine Learning Engineer, Prompt Engineer, AI Engineer, Full Stack Web Development, Big Data Engineering, Marketing Analyst, Human Resource Manager, Software Developer. Your task is to review the provided resume.
        Please share your professional evaluation on whether the candidate's profile aligns with the role by highlighting their strengths and weaknesses. Also mention the Skills they already have and suggest some skills to improve their resume and suggest some courses they might take to improve the skills.

        Resume:
        {resume_text}
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        # Update user recommendations
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.recommendations = response.text
        db.commit()

        return {"recommendations": response.text}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))