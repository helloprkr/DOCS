import pytest
from httpx import AsyncClient
from ..main import app
from ..database.db import init_db, cleanup_db
import uuid

# Test data
TEST_USER_ID = str(uuid.uuid4())

@pytest.fixture(autouse=True)
async def setup_database():
    """Set up a fresh test database for each test."""
    await init_db()
    yield
    await cleanup_db()

@pytest.fixture
async def client():
    """Create a test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_get_user_progress(client):
    """Test getting user progress."""
    response = await client.get(f"/api/users/{TEST_USER_ID}/progress")
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == TEST_USER_ID
    assert data["total_points"] == 0
    assert data["level"] == 1
    assert data["streak_days"] == 0

@pytest.mark.asyncio
async def test_award_points(client):
    """Test awarding points to a user."""
    points = 100
    activity = "test_activity"
    
    response = await client.post(
        f"/api/users/{TEST_USER_ID}/points",
        params={"points": points, "activity_type": activity}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_points"] == points
    assert activity in data["stats"]["activities"]
    assert data["stats"]["activities"][activity] == points

@pytest.mark.asyncio
async def test_update_streak(client):
    """Test updating user streak."""
    # Update streak
    response = await client.post(f"/api/users/{TEST_USER_ID}/streak")
    
    assert response.status_code == 200
    data = response.json()
    assert data["streak_days"] == 1
    
    # Update again (should still be 1 as it's the same day)
    response = await client.post(f"/api/users/{TEST_USER_ID}/streak")
    data = response.json()
    assert data["streak_days"] == 1

@pytest.mark.asyncio
async def test_check_achievements(client):
    """Test checking and awarding achievements."""
    # Award enough points to trigger an achievement
    await client.post(
        f"/api/users/{TEST_USER_ID}/points",
        params={"points": 1000, "activity_type": "test"}
    )
    
    # Check achievements
    response = await client.get(f"/api/users/{TEST_USER_ID}/achievements")
    
    assert response.status_code == 200
    achievements = response.json()
    assert len(achievements) > 0
    
    # Check achievement structure
    achievement = achievements[0]
    assert "name" in achievement
    assert "description" in achievement
    assert "points" in achievement
    assert "criteria" in achievement

@pytest.mark.asyncio
async def test_get_user_skills(client):
    """Test getting user skills."""
    response = await client.get(f"/api/users/{TEST_USER_ID}/skills")
    
    assert response.status_code == 200
    skills = response.json()
    assert isinstance(skills, list)
    
    if skills:  # If default skills are initialized
        skill = skills[0]
        assert "name" in skill
        assert "description" in skill
        assert "current_level" in skill
        assert "max_level" in skill
        assert "current_points" in skill
        assert "points_required" in skill

@pytest.mark.asyncio
async def test_add_skill_points(client):
    """Test adding points to a skill."""
    # First get available skills
    skills_response = await client.get(f"/api/users/{TEST_USER_ID}/skills")
    skills = skills_response.json()
    
    if skills:
        skill_id = skills[0]["skill_id"]
        points = 50
        
        # Add points to skill
        response = await client.post(
            f"/api/users/{TEST_USER_ID}/skills/{skill_id}/points",
            params={"points": points}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["skill_id"] == skill_id
        assert data["current_points"] == points

@pytest.mark.asyncio
async def test_get_user_stats(client):
    """Test getting comprehensive user statistics."""
    # Add some activity
    await client.post(
        f"/api/users/{TEST_USER_ID}/points",
        params={"points": 100, "activity_type": "test"}
    )
    await client.post(f"/api/users/{TEST_USER_ID}/streak")
    
    # Get stats
    response = await client.get(f"/api/users/{TEST_USER_ID}/stats")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check structure
    assert "progress" in data
    assert "level" in data["progress"]
    assert "total_points" in data["progress"]
    assert "streak_days" in data["progress"]
    
    assert "skills" in data
    assert isinstance(data["skills"], list)
    
    assert "stats" in data
    assert isinstance(data["stats"], dict)

@pytest.mark.asyncio
async def test_achievement_triggers(client):
    """Test that achievements are triggered correctly."""
    # Trigger streak achievement
    for _ in range(7):  # Simulate 7 days of activity
        await client.post(f"/api/users/{TEST_USER_ID}/streak")
        
    # Check achievements
    response = await client.get(f"/api/users/{TEST_USER_ID}/achievements")
    achievements = response.json()
    
    # Find streak achievement
    streak_achievement = next(
        (a for a in achievements if "streak" in a["name"].lower()),
        None
    )
    
    assert streak_achievement is not None
    assert streak_achievement["criteria"]["streak_days"] == 7 