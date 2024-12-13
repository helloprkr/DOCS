from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_
from sqlalchemy.orm import joinedload
from ..models.gamification import Achievement, Skill, UserSkill, Progress
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

class GamificationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_progress(self, user_id: str) -> Progress:
        """Get or create user progress."""
        stmt = select(Progress).where(Progress.user_id == user_id)
        result = await self.session.execute(stmt)
        progress = result.scalar_one_or_none()
        
        if not progress:
            progress = Progress(user_id=user_id)
            self.session.add(progress)
            await self.session.commit()
            
        return progress

    async def update_streak(self, user_id: str) -> int:
        """Update user's daily streak."""
        progress = await self.get_user_progress(user_id)
        
        # Check if last activity was yesterday
        yesterday = datetime.utcnow() - timedelta(days=1)
        if progress.last_activity.date() == yesterday.date():
            progress.streak_days += 1
        elif progress.last_activity.date() < yesterday.date():
            progress.streak_days = 1
            
        progress.last_activity = datetime.utcnow()
        await self.session.commit()
        return progress.streak_days

    async def award_points(self, user_id: str, points: int, activity_type: str) -> Progress:
        """Award points to user and update level."""
        progress = await self.get_user_progress(user_id)
        progress.total_points += points
        
        # Update level (simple level calculation)
        new_level = (progress.total_points // 1000) + 1
        if new_level > progress.level:
            progress.level = new_level
            
        # Update stats
        if not progress.stats:
            progress.stats = {}
        if 'activities' not in progress.stats:
            progress.stats['activities'] = {}
        
        if activity_type not in progress.stats['activities']:
            progress.stats['activities'][activity_type] = 0
        progress.stats['activities'][activity_type] += points
        
        await self.session.commit()
        return progress

    async def check_achievements(self, user_id: str) -> List[Achievement]:
        """Check and award new achievements."""
        progress = await self.get_user_progress(user_id)
        
        # Get all achievements
        stmt = select(Achievement).where(Achievement.user_id == user_id)
        result = await self.session.execute(stmt)
        current_achievements = result.scalars().all()
        
        # Define achievement criteria
        achievements_to_check = [
            {
                'name': 'First Note',
                'description': 'Created your first note',
                'criteria': {'notes_count': 1},
                'points': 100
            },
            {
                'name': 'Consistent Writer',
                'description': '7-day streak',
                'criteria': {'streak_days': 7},
                'points': 500
            },
            {
                'name': 'Tag Master',
                'description': 'Used 10 different tags',
                'criteria': {'unique_tags': 10},
                'points': 300
            }
        ]
        
        new_achievements = []
        
        # Check each achievement
        for achievement_data in achievements_to_check:
            # Skip if already achieved
            if any(a.name == achievement_data['name'] for a in current_achievements):
                continue
                
            # Check criteria
            criteria_met = True
            for key, value in achievement_data['criteria'].items():
                if key == 'streak_days' and progress.streak_days < value:
                    criteria_met = False
                elif key in progress.stats and progress.stats[key] < value:
                    criteria_met = False
                    
            if criteria_met:
                achievement = Achievement(
                    user_id=user_id,
                    name=achievement_data['name'],
                    description=achievement_data['description'],
                    criteria=achievement_data['criteria'],
                    points=achievement_data['points']
                )
                self.session.add(achievement)
                new_achievements.append(achievement)
                
                # Award points for achievement
                await self.award_points(user_id, achievement_data['points'], 'achievement')
        
        if new_achievements:
            await self.session.commit()
            
        return new_achievements

    async def get_or_create_user_skill(self, user_id: str, skill_id: str) -> UserSkill:
        """Get or create a user's skill."""
        stmt = select(UserSkill).where(
            and_(
                UserSkill.user_id == user_id,
                UserSkill.skill_id == skill_id
            )
        )
        result = await self.session.execute(stmt)
        user_skill = result.scalar_one_or_none()
        
        if not user_skill:
            user_skill = UserSkill(
                user_id=user_id,
                skill_id=skill_id
            )
            self.session.add(user_skill)
            await self.session.commit()
            
        return user_skill

    async def add_skill_points(self, user_id: str, skill_id: str, points: int) -> UserSkill:
        """Add points to a user's skill and check for level up."""
        user_skill = await self.get_or_create_user_skill(user_id, skill_id)
        
        # Add points
        user_skill.current_points += points
        
        # Check for level up
        stmt = select(Skill).where(Skill.id == skill_id)
        result = await self.session.execute(stmt)
        skill = result.scalar_one()
        
        while (user_skill.current_points >= skill.points_required and 
               user_skill.current_level < skill.max_level):
            user_skill.current_level += 1
            user_skill.current_points -= skill.points_required
            
        await self.session.commit()
        return user_skill

    async def get_user_skills(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all skills and their progress for a user."""
        stmt = select(UserSkill).options(
            joinedload(UserSkill.skill)
        ).where(UserSkill.user_id == user_id)
        
        result = await self.session.execute(stmt)
        user_skills = result.scalars().all()
        
        return [
            {
                'skill': user_skill.skill,
                'current_level': user_skill.current_level,
                'current_points': user_skill.current_points,
                'is_active': user_skill.is_active
            }
            for user_skill in user_skills
        ]
