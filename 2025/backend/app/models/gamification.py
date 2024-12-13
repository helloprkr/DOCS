from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.db import Base
import uuid

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    criteria = Column(JSON, nullable=False)  # JSON object defining achievement criteria
    points = Column(Integer, default=0)
    icon = Column(String)  # URL or path to achievement icon
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_id = Column(String, ForeignKey('users.id'))
    user = relationship("User", back_populates="achievements")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    level = Column(Integer, default=1)
    max_level = Column(Integer, default=10)
    points_required = Column(Integer, default=100)
    icon = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_skills = relationship("UserSkill", back_populates="skill")

class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'))
    skill_id = Column(String, ForeignKey('skills.id'))
    current_level = Column(Integer, default=1)
    current_points = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    skill = relationship("Skill", back_populates="user_skills")

class Progress(Base):
    __tablename__ = "progress"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'))
    total_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    streak_days = Column(Integer, default=0)
    last_activity = Column(DateTime, default=datetime.utcnow)
    stats = Column(JSON, default=dict)  # Additional statistics as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
