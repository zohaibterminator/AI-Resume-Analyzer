from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Enum
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    email_id = Column(String(500), nullable=False, unique=True, index=True)
    mobile_num = Column(String(100), nullable=False, unique=True, index=True)

    user_resume = relationship("Resume", back_populates="user", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resume"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    resume_score = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    no_of_pages = Column(Integer, nullable=False)
    recommendations = Column(Text)
    user_level = Column(String(255), nullable=False)
    total_experience = Column(Float, nullable=False)
    skills = Column(String(200), nullable=False)
    job_description = Column(String(200), nullable=False)

    user = relationship("User", back_populates="user_resume")