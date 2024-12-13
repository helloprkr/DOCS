from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.db import Base
import uuid

# Tags association table
note_tags = Table(
    'note_tags',
    Base.metadata,
    Column('note_id', String, ForeignKey('notes.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(String, ForeignKey('users.id'))
    
    # Relationships
    tags = relationship("Tag", secondary=note_tags, back_populates="notes")
    user = relationship("User", back_populates="notes")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationships
    notes = relationship("Note", secondary=note_tags, back_populates="tags")

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    notes = relationship("Note", back_populates="user")
    achievements = relationship("Achievement", back_populates="user")
