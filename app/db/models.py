from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Enum
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    email_id = Column(String(500), nullable=False, unique=True, index=True)
    resume_score = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    page_no = Column(Integer, nullable=False)
    recommendations = Column(Text)

    # Relationships
    attributes = relationship("UserAttributes", back_populates="user", cascade="all, delete-orphan")
    skills = relationship("Skill", back_populates="user", cascade="all, delete-orphan")


class UserAttributes(Base):
    __tablename__ = "user_attributes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    predicted_field = Column(String(255), nullable=False)
    user_level = Column(String(255), nullable=False)

    # Relationships
    user = relationship("User", back_populates="attributes")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(255), nullable=False)
    type = Column(Enum("Actual", "Recommended", name="skill_type"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="skills")