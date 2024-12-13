import pytest
from httpx import AsyncClient
from ..main import app
from ..database.db import init_db, cleanup_db
import uuid

# Test data
TEST_USER_ID = str(uuid.uuid4())
TEST_NOTE = {
    "title": "Test Note",
    "content": "This is a test note",
    "tags": ["test", "example"]
}

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
async def test_create_note(client):
    """Test creating a new note."""
    response = await client.post(
        f"/api/notes?user_id={TEST_USER_ID}",
        json=TEST_NOTE
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == TEST_NOTE["title"]
    assert data["content"] == TEST_NOTE["content"]
    assert len(data["tags"]) == len(TEST_NOTE["tags"])

@pytest.mark.asyncio
async def test_get_note(client):
    """Test getting a note by ID."""
    # First create a note
    create_response = await client.post(
        f"/api/notes?user_id={TEST_USER_ID}",
        json=TEST_NOTE
    )
    note_id = create_response.json()["id"]
    
    # Then get the note
    response = await client.get(f"/api/notes/{note_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == TEST_NOTE["title"]

@pytest.mark.asyncio
async def test_update_note(client):
    """Test updating a note."""
    # Create a note
    create_response = await client.post(
        f"/api/notes?user_id={TEST_USER_ID}",
        json=TEST_NOTE
    )
    note_id = create_response.json()["id"]
    
    # Update the note
    updated_data = {
        "title": "Updated Title",
        "content": "Updated content"
    }
    response = await client.put(
        f"/api/notes/{note_id}",
        json=updated_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_data["title"]
    assert data["content"] == updated_data["content"]

@pytest.mark.asyncio
async def test_delete_note(client):
    """Test deleting a note."""
    # Create a note
    create_response = await client.post(
        f"/api/notes?user_id={TEST_USER_ID}",
        json=TEST_NOTE
    )
    note_id = create_response.json()["id"]
    
    # Delete the note
    response = await client.delete(f"/api/notes/{note_id}")
    assert response.status_code == 200
    
    # Verify note is deleted
    get_response = await client.get(f"/api/notes/{note_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_search_notes(client):
    """Test searching notes."""
    # Create some test notes
    await client.post(
        f"/api/notes?user_id={TEST_USER_ID}",
        json={
            "title": "Search Test 1",
            "content": "This note should be found",
            "tags": ["search"]
        }
    )
    await client.post(
        f"/api/notes?user_id={TEST_USER_ID}",
        json={
            "title": "Search Test 2",
            "content": "This note should not be found",
            "tags": ["search"]
        }
    )
    
    # Search for notes
    response = await client.get(
        f"/api/users/{TEST_USER_ID}/notes/search?query=should+be+found"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "should be found" in data[0]["content"]

@pytest.mark.asyncio
async def test_get_user_tags(client):
    """Test getting all tags for a user."""
    # Create notes with tags
    await client.post(
        f"/api/notes?user_id={TEST_USER_ID}",
        json={
            "title": "Tag Test 1",
            "content": "Content 1",
            "tags": ["tag1", "tag2"]
        }
    )
    await client.post(
        f"/api/notes?user_id={TEST_USER_ID}",
        json={
            "title": "Tag Test 2",
            "content": "Content 2",
            "tags": ["tag2", "tag3"]
        }
    )
    
    # Get user tags
    response = await client.get(f"/api/users/{TEST_USER_ID}/tags")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3  # Should have 3 unique tags
    tag_names = {tag["name"] for tag in data}
    assert tag_names == {"tag1", "tag2", "tag3"} 