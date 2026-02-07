# Data Model: Task CRUD Operations

**Feature**: Task CRUD Operations
**Date**: 2026-01-12
**Status**: Complete

## Overview

This document defines the database schema, entity relationships, and data validation rules for the Task CRUD operations feature.

## Entity Definitions

### Task Entity

**Purpose**: Represents a single task or to-do item owned by a user.

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL, DEFAULT gen_random_uuid() | Unique identifier for the task |
| `user_id` | UUID | FOREIGN KEY (users.id), NOT NULL, INDEXED | Owner of the task |
| `title` | VARCHAR(500) | NOT NULL, LENGTH 1-500 | Task title/summary |
| `description` | TEXT | NULLABLE, MAX LENGTH 2000 | Detailed task description |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Task status (pending, in_progress, completed) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last modification timestamp |

**Indexes**:
- Primary index on `id`
- Foreign key index on `user_id` (for fast user-scoped queries)
- Index on `status` (for filtering by status)
- Composite index on `(user_id, created_at DESC)` (for paginated list queries)

**Constraints**:
- `user_id` must reference an existing user in the `users` table
- `title` cannot be empty string
- `status` must be one of: 'pending', 'in_progress', 'completed'
- `created_at` is immutable after creation
- `updated_at` is automatically updated on every modification

### User Entity (Reference)

**Purpose**: Represents an authenticated user of the system (defined in authentication feature).

**Relevant Attributes**:
- `id`: UUID (PRIMARY KEY)
- `email`: VARCHAR(255) (UNIQUE, NOT NULL)
- `created_at`: TIMESTAMP

**Note**: User entity is managed by the authentication system. Task feature only references it via foreign key.

## Relationships

### Task → User (Many-to-One)

- **Cardinality**: Many tasks belong to one user
- **Foreign Key**: `tasks.user_id` → `users.id`
- **Cascade**: ON DELETE CASCADE (when user is deleted, all their tasks are deleted)
- **Enforcement**: Database-level foreign key constraint + application-level validation

**Relationship Rules**:
1. Every task must have exactly one owner (user_id is NOT NULL)
2. A user can have zero or many tasks
3. Tasks cannot be transferred between users (no ownership change)
4. Deleting a user automatically deletes all their tasks

## Database Schema (SQL)

```sql
-- Task table definition
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(500) NOT NULL CHECK (LENGTH(title) > 0),
    description TEXT CHECK (description IS NULL OR LENGTH(description) <= 2000),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Foreign key constraint
    CONSTRAINT fk_tasks_user FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);

-- Trigger to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## SQLModel Definitions (Python)

```python
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship

class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskBase(SQLModel):
    """Base task model with shared fields"""
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)

class Task(TaskBase, table=True):
    """Task database model"""
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to User (defined in auth module)
    # user: "User" = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass

class TaskUpdate(SQLModel):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[TaskStatus] = None

class TaskRead(TaskBase):
    """Schema for reading a task"""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

class TaskListResponse(SQLModel):
    """Schema for paginated task list response"""
    items: list[TaskRead]
    total: int
    page: int
    page_size: int
    total_pages: int
```

## TypeScript Definitions (Frontend)

```typescript
// Task status enum
export enum TaskStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed'
}

// Task interface
export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}

// Task creation payload
export interface TaskCreate {
  title: string;
  description?: string;
  status?: TaskStatus;
}

// Task update payload
export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: TaskStatus;
}

// Paginated task list response
export interface TaskListResponse {
  items: Task[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
```

## Validation Rules

### Title Validation
- **Required**: Yes
- **Min Length**: 1 character
- **Max Length**: 500 characters
- **Allowed Characters**: Any Unicode characters
- **Trimming**: Leading/trailing whitespace should be trimmed before validation
- **Error Message**: "Title is required and must be between 1 and 500 characters"

### Description Validation
- **Required**: No (optional field)
- **Min Length**: 0 characters (can be empty)
- **Max Length**: 2000 characters
- **Allowed Characters**: Any Unicode characters
- **Null vs Empty**: Both null and empty string are valid
- **Error Message**: "Description must not exceed 2000 characters"

### Status Validation
- **Required**: Yes (defaults to 'pending')
- **Allowed Values**: 'pending', 'in_progress', 'completed'
- **Case Sensitivity**: Lowercase only
- **Error Message**: "Status must be one of: pending, in_progress, completed"

### User ID Validation
- **Required**: Yes
- **Format**: Valid UUID v4
- **Existence Check**: Must reference existing user in database
- **Authorization**: Must match authenticated user's ID from JWT
- **Error Message**: "Invalid user ID or unauthorized access"

## State Transitions

### Task Status State Machine

```
[pending] ──────────────────────────────────────────────> [completed]
    │                                                           │
    │                                                           │
    └──────────────> [in_progress] ──────────────────────────> │
                            │                                  │
                            └──────────────────────────────────┘
```

**Allowed Transitions**:
- pending → in_progress
- pending → completed
- in_progress → completed
- in_progress → pending (restart)
- completed → pending (reopen)
- completed → in_progress (reopen and continue)

**Note**: All transitions are allowed (no restrictions). Users can move tasks between any states.

## Query Patterns

### List User's Tasks (Paginated)
```sql
SELECT * FROM tasks
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT $2 OFFSET $3;
```

### Get Single Task
```sql
SELECT * FROM tasks
WHERE id = $1 AND user_id = $2;
```

### Create Task
```sql
INSERT INTO tasks (user_id, title, description, status)
VALUES ($1, $2, $3, $4)
RETURNING *;
```

### Update Task
```sql
UPDATE tasks
SET title = $1, description = $2, status = $3, updated_at = NOW()
WHERE id = $4 AND user_id = $5
RETURNING *;
```

### Delete Task
```sql
DELETE FROM tasks
WHERE id = $1 AND user_id = $2
RETURNING id;
```

### Count User's Tasks
```sql
SELECT COUNT(*) FROM tasks
WHERE user_id = $1;
```

## Performance Considerations

1. **Indexing Strategy**:
   - Primary index on `id` for fast lookups
   - Index on `user_id` for user-scoped queries
   - Composite index on `(user_id, created_at DESC)` for paginated lists

2. **Query Optimization**:
   - Always include `user_id` in WHERE clause for data isolation
   - Use LIMIT/OFFSET for pagination
   - Select only needed columns when possible

3. **Connection Pooling**:
   - Reuse database connections via connection pool
   - Configure appropriate pool size (10-20 connections)

4. **Caching Strategy** (Future Enhancement):
   - Cache frequently accessed tasks in Redis
   - Invalidate cache on task updates/deletes
   - TTL of 5 minutes for cached data

## Migration Strategy

### Initial Migration (Create Tables)
```sql
-- Run this migration to create the tasks table
-- Migration: 001_create_tasks_table.sql

CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(500) NOT NULL CHECK (LENGTH(title) > 0),
    description TEXT CHECK (description IS NULL OR LENGTH(description) <= 2000),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'completed')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_tasks_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### Rollback Migration (Drop Tables)
```sql
-- Rollback migration: 001_drop_tasks_table.sql

DROP TRIGGER IF EXISTS update_tasks_updated_at ON tasks;
DROP FUNCTION IF EXISTS update_updated_at_column();
DROP TABLE IF EXISTS tasks CASCADE;
```

## Data Integrity

1. **Foreign Key Constraints**: Ensure tasks always reference valid users
2. **Check Constraints**: Validate status values and field lengths at database level
3. **NOT NULL Constraints**: Prevent null values in required fields
4. **Unique Constraints**: None (tasks don't need to be unique)
5. **Cascade Deletes**: Automatically delete tasks when user is deleted

## Security Considerations

1. **Data Isolation**: All queries must filter by `user_id`
2. **Authorization**: Verify JWT user_id matches path parameter
3. **SQL Injection**: Use parameterized queries (ORM handles this)
4. **Mass Assignment**: Only allow updating specific fields (title, description, status)
5. **Audit Trail**: Track creation and modification timestamps

## Testing Data

### Sample Tasks for Testing

```sql
-- Insert sample tasks for testing (user_id must exist)
INSERT INTO tasks (user_id, title, description, status) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'Buy groceries', 'Milk, eggs, bread', 'pending'),
('550e8400-e29b-41d4-a716-446655440000', 'Call dentist', 'Schedule annual checkup', 'in_progress'),
('550e8400-e29b-41d4-a716-446655440000', 'Finish project report', 'Due Friday', 'completed');
```
