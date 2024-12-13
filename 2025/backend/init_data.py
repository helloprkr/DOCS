import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import init_db, async_session
from models.note import Tag
from models.gamification import Skill, Achievement
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_tags(session: AsyncSession):
    """Initialize default tags."""
    default_tags = [
        "work", "personal", "ideas", "todo", "important",
        "project", "meeting", "research", "learning", "goals"
    ]
    
    for tag_name in default_tags:
        tag = Tag(name=tag_name)
        session.add(tag)
    
    await session.commit()
    logger.info("Default tags initialized")

async def init_skills(session: AsyncSession):
    """Initialize default skills."""
    default_skills = [
        {
            "name": "Writing",
            "description": "Ability to create clear and effective notes",
            "points_required": 100,
            "max_level": 10,
            "icon": "✍️"
        },
        {
            "name": "Organization",
            "description": "Skill in organizing and categorizing notes",
            "points_required": 150,
            "max_level": 10,
            "icon": "📋"
        },
        {
            "name": "Consistency",
            "description": "Regular note-taking habit",
            "points_required": 200,
            "max_level": 10,
            "icon": "📅"
        }
    ]
    
    for skill_data in default_skills:
        skill = Skill(**skill_data)
        session.add(skill)
    
    await session.commit()
    logger.info("Default skills initialized")

async def init_achievements(session: AsyncSession):
    """Initialize default achievements."""
    default_achievements = [
        {
            "name": "First Note",
            "description": "Created your first note",
            "criteria": {"notes_count": 1},
            "points": 100,
            "icon": "🎉"
        },
        {
            "name": "Consistent Writer",
            "description": "Maintained a 7-day writing streak",
            "criteria": {"streak_days": 7},
            "points": 500,
            "icon": "✨"
        },
        {
            "name": "Tag Master",
            "description": "Used 10 different tags",
            "criteria": {"unique_tags": 10},
            "points": 300,
            "icon": "🏷️"
        }
    ]
    
    for achievement_data in default_achievements:
        achievement = Achievement(**achievement_data)
        session.add(achievement)
    
    await session.commit()
    logger.info("Default achievements initialized")

async def main():
    """Initialize the database with default data."""
    try:
        # Initialize database schema
        await init_db()
        logger.info("Database schema initialized")
        
        # Initialize default data
        async with async_session() as session:
            await init_tags(session)
            await init_skills(session)
            await init_achievements(session)
            
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 