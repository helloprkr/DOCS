from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from ..database.db import get_session
from ..services.gamification_service import GamificationService

router = APIRouter()

class ProgressResponse(BaseModel):
    id: str
    user_id: str
    total_points: int
    level: int
    streak_days: int
    last_activity: datetime
    stats: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AchievementResponse(BaseModel):
    id: str
    name: str
    description: str
    criteria: Dict[str, Any]
    points: int
    icon: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class SkillResponse(BaseModel):
    skill_id: str
    name: str
    description: str
    current_level: int
    max_level: int
    current_points: int
    points_required: int
    icon: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/users/{user_id}/progress", response_model=ProgressResponse)
async def get_user_progress(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get user's progress information."""
    gamification_service = GamificationService(session)
    progress = await gamification_service.get_user_progress(user_id)
    return progress

@router.post("/users/{user_id}/points")
async def award_points(
    user_id: str,
    points: int = Query(..., description="Points to award"),
    activity_type: str = Query(..., description="Type of activity"),
    session: AsyncSession = Depends(get_session)
):
    """Award points to a user."""
    gamification_service = GamificationService(session)
    progress = await gamification_service.award_points(user_id, points, activity_type)
    return progress

@router.post("/users/{user_id}/streak")
async def update_user_streak(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Update user's daily streak."""
    gamification_service = GamificationService(session)
    streak_days = await gamification_service.update_streak(user_id)
    return {"streak_days": streak_days}

@router.get("/users/{user_id}/achievements", response_model=List[AchievementResponse])
async def check_achievements(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Check and return new achievements."""
    gamification_service = GamificationService(session)
    achievements = await gamification_service.check_achievements(user_id)
    return achievements

@router.get("/users/{user_id}/skills", response_model=List[SkillResponse])
async def get_user_skills(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get all skills and their progress for a user."""
    gamification_service = GamificationService(session)
    skills = await gamification_service.get_user_skills(user_id)
    return skills

@router.post("/users/{user_id}/skills/{skill_id}/points")
async def add_skill_points(
    user_id: str,
    skill_id: str,
    points: int = Query(..., description="Points to add to the skill"),
    session: AsyncSession = Depends(get_session)
):
    """Add points to a user's skill."""
    gamification_service = GamificationService(session)
    user_skill = await gamification_service.add_skill_points(user_id, skill_id, points)
    
    return {
        "skill_id": skill_id,
        "current_level": user_skill.current_level,
        "current_points": user_skill.current_points
    }

@router.get("/users/{user_id}/stats")
async def get_user_stats(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get comprehensive user statistics."""
    gamification_service = GamificationService(session)
    progress = await gamification_service.get_user_progress(user_id)
    skills = await gamification_service.get_user_skills(user_id)
    
    return {
        "progress": {
            "level": progress.level,
            "total_points": progress.total_points,
            "streak_days": progress.streak_days
        },
        "skills": skills,
        "stats": progress.stats
    }
