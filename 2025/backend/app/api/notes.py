from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from ..database.db import get_session
from ..services.note_service import NoteService
from ..services.gamification_service import GamificationService

router = APIRouter()

class TagBase(BaseModel):
    name: str

class NoteBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class NoteResponse(NoteBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.post("/notes", response_model=NoteResponse)
async def create_note(
    note: NoteCreate,
    user_id: str = Query(..., description="User ID"),
    session: AsyncSession = Depends(get_session)
):
    """Create a new note."""
    note_service = NoteService(session)
    gamification_service = GamificationService(session)
    
    # Create note
    created_note = await note_service.create_note(
        user_id=user_id,
        title=note.title,
        content=note.content,
        tags=note.tags
    )
    
    # Update user progress
    await gamification_service.award_points(user_id, 10, "note_creation")
    await gamification_service.update_streak(user_id)
    await gamification_service.check_achievements(user_id)
    
    return created_note

@router.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get a note by ID."""
    note_service = NoteService(session)
    note = await note_service.get_note(note_id)
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    return note

@router.get("/users/{user_id}/notes", response_model=List[NoteResponse])
async def get_user_notes(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get all notes for a user."""
    note_service = NoteService(session)
    notes = await note_service.get_user_notes(user_id)
    return notes

@router.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    note_update: NoteUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update a note."""
    note_service = NoteService(session)
    updated_note = await note_service.update_note(
        note_id=note_id,
        title=note_update.title,
        content=note_update.content,
        tags=note_update.tags
    )
    
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    return updated_note

@router.delete("/notes/{note_id}")
async def delete_note(
    note_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Delete a note."""
    note_service = NoteService(session)
    success = await note_service.delete_note(note_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
        
    return {"message": "Note deleted successfully"}

@router.get("/users/{user_id}/notes/search")
async def search_notes(
    user_id: str,
    query: str = Query(..., description="Search query"),
    session: AsyncSession = Depends(get_session)
):
    """Search user's notes."""
    note_service = NoteService(session)
    notes = await note_service.search_notes(user_id, query)
    return notes

@router.get("/users/{user_id}/tags")
async def get_user_tags(
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get all tags used by a user."""
    note_service = NoteService(session)
    tags = await note_service.get_user_tags(user_id)
    return tags

@router.get("/users/{user_id}/notes/tag/{tag_name}")
async def get_notes_by_tag(
    user_id: str,
    tag_name: str,
    session: AsyncSession = Depends(get_session)
):
    """Get all notes with a specific tag."""
    note_service = NoteService(session)
    notes = await note_service.get_notes_by_tag(user_id, tag_name)
    return notes
