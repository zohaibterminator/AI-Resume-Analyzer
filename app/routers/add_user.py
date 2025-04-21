from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from routers.schemas.models import User
from db.database import get_db
from db import models


router = APIRouter()

@router.post("/")
async def generate_recommendations(user: User, user_id: int, db: Session = Depends(get_db)):
    try:
        user = models.User(
            name=user.name,
            email_id=user.email_id,
            mobile_num=user.mobile_num,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "message": "user added successfully",
            "user_id": user.id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))