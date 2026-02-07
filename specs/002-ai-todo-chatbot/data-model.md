# Data Model Specification: AI Todo Chatbot

**Feature**: 002-ai-todo-chatbot
**Date**: 2026-02-05
**Purpose**: Define database schema and SQLModel models for conversation and message storage

## Overview

This document specifies the data models required for the AI Todo Chatbot feature. The system adds two new tables (conversations, messages) to the existing database schema while maintaining compatibility with existing User and Task models.

## Existing Models (No Changes)

### User Model

```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Relationships**:
- One-to-many with Conversation (user owns multiple conversations)
- One-to-many with Task (user owns multiple tasks)

### Task Model

```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: str = Field(default=TaskStatus.PENDING.value, max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Relationships**:
- Many-to-one with User (task belongs to one user)

## New Models

### Conversation Model

```python
class Conversation(SQLModel, table=True):
    """
    Represents a chat conversation between a user and the AI assistant.
    Each conversation contains multiple messages and belongs to one user.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        description="Owner of the conversation"
    )
    title: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Auto-generated from first user message"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Conversation start time"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last message time"
    )
```

**Field Descriptions**:
- `id`: Primary key, auto-incremented
- `user_id`: Foreign key to users table, indexed for fast user conversation lookups
- `title`: Optional conversation title, auto-generated from first user message (e.g., "Todo management" or first 50 chars of first message)
- `created_at`: Timestamp when conversation was created
- `updated_at`: Timestamp of last message in conversation (updated on each new message)

**Relationships**:
- Many-to-one with User (conversation belongs to one user)
- One-to-many with Message (conversation contains multiple messages)

**Indexes**:
- Primary key index on `id` (automatic)
- Index on `user_id` for fast user conversation queries
- Composite index on `(user_id, updated_at DESC)` for recent conversations list

**Constraints**:
- `user_id` must reference existing user (foreign key constraint)
- `title` max length 200 characters
- `created_at` and `updated_at` cannot be null

### Message Model

```python
class Message(SQLModel, table=True):
    """
    Represents a single message in a conversation.
    Messages can be from the user or the AI assistant.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(
        foreign_key="conversations.id",
        index=True,
        description="Conversation this message belongs to"
    )
    role: str = Field(
        max_length=20,
        description="Message sender: 'user' or 'assistant'"
    )
    content: str = Field(
        max_length=10000,
        description="Message text content"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Message timestamp"
    )
```

**Field Descriptions**:
- `id`: Primary key, auto-incremented
- `conversation_id`: Foreign key to conversations table, indexed for fast message loading
- `role`: Message sender role, either "user" or "assistant"
- `content`: Message text content, max 10,000 characters
- `created_at`: Timestamp when message was created

**Relationships**:
- Many-to-one with Conversation (message belongs to one conversation)

**Indexes**:
- Primary key index on `id` (automatic)
- Index on `conversation_id` for fast conversation message queries
- Composite index on `(conversation_id, created_at ASC)` for chronological message loading

**Constraints**:
- `conversation_id` must reference existing conversation (foreign key constraint)
- `role` must be either "user" or "assistant" (application-level validation)
- `content` max length 10,000 characters
- `created_at` cannot be null

## Database Schema Diagram

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │
│ email           │
│ password_hash   │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │ 1:N
         │
    ┌────┴─────────────────────┐
    │                          │
    │                          │
┌───▼──────────┐      ┌────────▼────────┐
│    tasks     │      │  conversations  │
├──────────────┤      ├─────────────────┤
│ id (PK)      │      │ id (PK)         │
│ user_id (FK) │      │ user_id (FK)    │
│ title        │      │ title           │
│ description  │      │ created_at      │
│ status       │      │ updated_at      │
│ created_at   │      └────────┬────────┘
│ updated_at   │               │
└──────────────┘               │ 1:N
                               │
                      ┌────────▼────────┐
                      │    messages     │
                      ├─────────────────┤
                      │ id (PK)         │
                      │ conversation_id │
                      │ role            │
                      │ content         │
                      │ created_at      │
                      └─────────────────┘
```

## SQL Migration Script

```sql
-- Create conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create index on user_id for fast user conversation lookups
CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Create composite index for recent conversations
CREATE INDEX idx_conversations_user_updated ON conversations(user_id, updated_at DESC);

-- Create messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL CHECK (LENGTH(content) <= 10000),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create index on conversation_id for fast message loading
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);

-- Create composite index for chronological message loading
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at ASC);
```

## SQLModel Implementation

### File: backend/models.py

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

# Existing models (no changes)
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: str = Field(default=TaskStatus.PENDING.value, max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# New models
class Conversation(SQLModel, table=True):
    """Chat conversation between user and AI assistant."""
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    """Single message in a conversation."""
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str = Field(max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## Pydantic Schemas

### File: backend/schemas.py (additions)

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# Chat request/response schemas
class ChatRequest(BaseModel):
    """Request schema for /api/chat endpoint."""
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_id: Optional[int] = Field(None, description="Existing conversation ID")

class ChatResponse(BaseModel):
    """Response schema for /api/chat endpoint."""
    conversation_id: int
    response: str
    created_at: datetime

# Conversation schemas
class ConversationPublic(BaseModel):
    """Public conversation representation."""
    id: int
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ConversationList(BaseModel):
    """List of conversations."""
    conversations: List[ConversationPublic]
    total: int

# Message schemas
class MessagePublic(BaseModel):
    """Public message representation."""
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationHistory(BaseModel):
    """Conversation with full message history."""
    conversation: ConversationPublic
    messages: List[MessagePublic]
```

## Data Access Patterns

### User-Scoped Queries

All queries must enforce user-level data isolation:

```python
# Get user's conversations
def get_user_conversations(user_id: int, session: Session) -> List[Conversation]:
    statement = select(Conversation).where(
        Conversation.user_id == user_id
    ).order_by(Conversation.updated_at.desc())
    return session.exec(statement).all()

# Get conversation with ownership check
def get_conversation(conversation_id: int, user_id: int, session: Session) -> Optional[Conversation]:
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id  # Ownership check
    )
    return session.exec(statement).first()

# Load conversation messages
def get_conversation_messages(conversation_id: int, limit: int = 20, session: Session) -> List[Message]:
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.desc()).limit(limit)
    messages = session.exec(statement).all()
    return list(reversed(messages))  # Return chronological order
```

### Conversation Creation

```python
def create_conversation(user_id: int, first_message: str, session: Session) -> Conversation:
    # Generate title from first message (first 50 chars)
    title = first_message[:50] + "..." if len(first_message) > 50 else first_message

    conversation = Conversation(
        user_id=user_id,
        title=title,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation
```

### Message Persistence

```python
def add_message(conversation_id: int, role: str, content: str, session: Session) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        created_at=datetime.utcnow()
    )
    session.add(message)

    # Update conversation updated_at
    conversation = session.get(Conversation, conversation_id)
    if conversation:
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)

    session.commit()
    session.refresh(message)
    return message
```

## Data Validation

### Application-Level Validation

```python
# Validate message role
def validate_message_role(role: str) -> bool:
    return role in ["user", "assistant"]

# Validate message content length
def validate_message_content(content: str) -> bool:
    return 1 <= len(content) <= 10000

# Validate conversation ownership
def validate_conversation_ownership(conversation_id: int, user_id: int, session: Session) -> bool:
    conversation = session.get(Conversation, conversation_id)
    return conversation is not None and conversation.user_id == user_id
```

## Performance Considerations

### Query Optimization

1. **Index Usage**:
   - `conversations.user_id` index for user conversation lists
   - `messages.conversation_id` index for message loading
   - Composite indexes for sorted queries

2. **Limit Conversation History**:
   - Load only last 20 messages by default
   - Implement pagination for older messages if needed

3. **Connection Pooling**:
   - Reuse existing database connection pool
   - Configure pool size based on expected load

### Storage Estimates

**Per User**:
- Average 10 conversations
- Average 15 messages per conversation
- Average 100 bytes per message

**Storage per user**: ~15 KB
**1000 users**: ~15 MB
**10,000 users**: ~150 MB

**Conclusion**: Storage requirements are minimal, database performance should not be a concern.

## Migration Strategy

### Development Environment

```bash
# Run migration script
psql $DATABASE_URL < migrations/add_chat_tables.sql

# Or use SQLModel
python -c "from db import create_db_and_tables; create_db_and_tables()"
```

### Production Environment

1. Backup database
2. Run migration script during maintenance window
3. Verify tables created with correct indexes
4. Test with sample data
5. Deploy application code

## Data Retention Policy

**Conversations**: Retain indefinitely (user-initiated deletion only)
**Messages**: Retain indefinitely (part of conversation history)

**Future Considerations**:
- Implement conversation archival after 90 days of inactivity
- Implement message pruning for very long conversations (>100 messages)
- Add soft delete for conversations (deleted_at timestamp)

## Security Considerations

1. **User Data Isolation**: All queries enforce user_id filtering
2. **SQL Injection**: SQLModel parameterized queries prevent injection
3. **Content Validation**: Message content length limits prevent abuse
4. **Cascade Deletion**: Deleting user cascades to conversations and messages

---

**Data Model Status**: Complete and ready for implementation
**Next Step**: Create API contracts (chat-api.yaml, mcp-tools.yaml)
