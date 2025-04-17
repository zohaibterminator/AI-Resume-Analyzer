from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import models
from routers.schemas.models import Resume
from fastapi import Depends

router = APIRouter()

@router.post("/")
async def upload_resume(resume: Resume, db: Session = Depends(get_db)):
    try:
        # Create new user entry
        user = models.User(
            name=resume.name,
            email=resume.email,
            resume_score=resume.resume_score,
            timestamp=resume.timestamp,
            page_no=resume.page_no
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # User attributes
        attr = models.UserAttribute(
            user_id=user.id,
            predicted_field=resume.predicted_field,
            user_level=resume.user_level
        )
        db.add(attr)

        # Skills
        for skill in resume.actual_skills:
            db.add(models.Skill(user_id=user.id, skill_name=skill, type="Actual"))

        for skill in resume.recommended_skills:
            db.add(models.Skill(user_id=user.id, skill_name=skill, type="Recommended"))

        db.commit()
        return {"message": "Resume uploaded successfully", "user_id": user.id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))