from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from ..models.note import Note, Tag
from typing import List, Optional
from datetime import datetime

class NoteService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_note(self, user_id: str, title: str, content: str, tags: List[str] = None) -> Note:
        """Create a new note with optional tags."""
        # Create note
        note = Note(
            title=title,
            content=content,
            user_id=user_id
        )
        
        # Handle tags
        if tags:
            for tag_name in tags:
                # Get or create tag
                stmt = select(Tag).where(Tag.name == tag_name)
                result = await self.session.execute(stmt)
                tag = result.scalar_one_or_none()
                
                if not tag:
                    tag = Tag(name=tag_name)
                    self.session.add(tag)
                
                note.tags.append(tag)
        
        self.session.add(note)
        await self.session.commit()
        await self.session.refresh(note)
        return note

    async def get_note(self, note_id: str) -> Optional[Note]:
        """Get a note by ID with tags."""
        stmt = select(Note).options(joinedload(Note.tags)).where(Note.id == note_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_notes(self, user_id: str) -> List[Note]:
        """Get all notes for a user."""
        stmt = select(Note).options(joinedload(Note.tags)).where(Note.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_note(self, note_id: str, title: Optional[str] = None, 
                         content: Optional[str] = None, tags: List[str] = None) -> Optional[Note]:
        """Update a note and its tags."""
        note = await self.get_note(note_id)
        if not note:
            return None
            
        # Update basic fields
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        note.updated_at = datetime.utcnow()
        
        # Update tags if provided
        if tags is not None:
            # Clear existing tags
            note.tags = []
            
            # Add new tags
            for tag_name in tags:
                stmt = select(Tag).where(Tag.name == tag_name)
                result = await self.session.execute(stmt)
                tag = result.scalar_one_or_none()
                
                if not tag:
                    tag = Tag(name=tag_name)
                    self.session.add(tag)
                
                note.tags.append(tag)
        
        await self.session.commit()
        await self.session.refresh(note)
        return note

    async def delete_note(self, note_id: str) -> bool:
        """Delete a note by ID."""
        stmt = delete(Note).where(Note.id == note_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def search_notes(self, user_id: str, query: str) -> List[Note]:
        """Search notes by content."""
        stmt = select(Note).options(joinedload(Note.tags)).where(
            Note.user_id == user_id,
            Note.content.ilike(f"%{query}%")
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_notes_by_tag(self, user_id: str, tag_name: str) -> List[Note]:
        """Get all notes with a specific tag."""
        stmt = select(Note).options(joinedload(Note.tags)).join(Note.tags).where(
            Note.user_id == user_id,
            Tag.name == tag_name
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_tags(self, user_id: str) -> List[Tag]:
        """Get all tags used by a user."""
        stmt = select(Tag).join(Tag.notes).where(Note.user_id == user_id).distinct()
        result = await self.session.execute(stmt)
        return result.scalars().all()
