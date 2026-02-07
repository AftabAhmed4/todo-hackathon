"""
Pydantic request/response schemas for authentication and tasks.

Defines data models for API requests and responses.
"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from models import TaskStatus


class SignupRequest(BaseModel):
    """Request schema for user signup."""
    email: EmailStr = Field(..., max_length=255, description="User's email address")
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User's password (min 8 chars, must include uppercase, lowercase, number)"
    )


class SigninRequest(BaseModel):
    """Request schema for user signin."""
    email: EmailStr = Field(..., max_length=255, description="User's email address")
    password: str = Field(..., description="User's password")


class UserPublic(BaseModel):
    """Public user representation (safe for API responses)."""
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Response schema for authentication endpoints."""
    user: UserPublic
    token: str
    message: str


# Task Schemas

class TaskCreate(BaseModel):
    """Request schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=500, description="Task title (required)")
    description: Optional[str] = Field(None, max_length=2000, description="Task description (optional)")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")


class TaskUpdate(BaseModel):
    """Request schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=500, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")


class TaskRead(BaseModel):
    """Response schema for reading a task."""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Response schema for paginated task list."""
    items: List[TaskRead]
    total: int
    page: int
    page_size: int
    total_pages: int
