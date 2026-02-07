"""
User and Task models for the application.

Represents user accounts and their tasks with proper data isolation.
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class User(SQLModel, table=True):
    """
    User account entity for authentication.

    Represents an individual user with email/password credentials.
    Each user has a unique ID used for data isolation in future features.
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User's email address (unique, used for login)"
    )
    password_hash: str = Field(
        max_length=255,
        description="Bcrypt hash of user's password (never store plaintext)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC)"
    )


class Task(SQLModel, table=True):
    """
    Task entity for user's to-do items.

    Each task belongs to a specific user and includes title, description, and status.
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        description="Owner of the task (foreign key to users.id)"
    )
    title: str = Field(
        max_length=500,
        description="Task title (required, max 500 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Task description (optional, max 2000 characters)"
    )
    status: str = Field(
        default=TaskStatus.PENDING.value,
        max_length=20,
        description="Task status (pending, in_progress, completed)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC)"
    )


class Conversation(SQLModel, table=True):
    """
    Conversation entity for AI chatbot interactions.

    Each conversation belongs to a specific user and contains multiple messages.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        description="Owner of the conversation (foreign key to users.id)"
    )
    title: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Conversation title (optional, auto-generated from first message)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Conversation creation timestamp (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC)"
    )


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(SQLModel, table=True):
    """
    Message entity for individual chat messages.

    Each message belongs to a conversation and has a role (user/assistant/system).
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(
        foreign_key="conversations.id",
        index=True,
        description="Parent conversation (foreign key to conversations.id)"
    )
    role: str = Field(
        max_length=20,
        description="Message role (user, assistant, or system)"
    )
    content: str = Field(
        description="Message content (text)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Message creation timestamp (UTC)"
    )
