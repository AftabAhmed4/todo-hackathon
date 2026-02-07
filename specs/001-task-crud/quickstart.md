# Developer Quickstart: Task CRUD Operations

**Feature**: Task CRUD Operations
**Date**: 2026-01-12
**Status**: Complete

## Overview

This guide provides step-by-step instructions for setting up the development environment and implementing the Task CRUD operations feature.

## Prerequisites

### Required Software
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **PostgreSQL**: 14 or higher (or Neon Serverless PostgreSQL account)
- **Git**: Latest version

### Required Accounts
- **Neon Database**: Sign up at https://neon.tech for serverless PostgreSQL
- **Better Auth**: Configured in the project for JWT authentication

## Project Structure

```
hackathon-todo/
├── backend/              # FastAPI backend
│   ├── models.py         # SQLModel database models
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── routes/           # API route handlers
│   │   └── tasks.py      # Task CRUD endpoints
│   ├── auth.py           # JWT verification middleware
│   ├── db.py             # Database connection
│   ├── main.py           # FastAPI app entry point
│   ├── requirements.txt  # Python dependencies
│   └── .env              # Environment variables (not in git)
├── frontend/             # Next.js frontend
│   ├── app/              # Next.js App Router pages
│   ├── components/       # React components
│   ├── lib/              # Utility functions and API client
│   ├── package.json      # Node dependencies
│   └── .env.local        # Environment variables (not in git)
└── specs/                # Feature specifications
    └── 001-task-crud/    # This feature's documentation
```

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies**:
- FastAPI 0.104+
- SQLModel 0.0.14
- python-jose[cryptography] 3.3.0
- passlib[bcrypt] 1.7.4
- psycopg2-binary 2.9.9
- uvicorn[standard] 0.24.0

### 4. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Database connection
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Authentication
BETTER_AUTH_SECRET=your-secret-key-here

# Server configuration
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

**Getting DATABASE_URL from Neon**:
1. Log in to https://console.neon.tech
2. Create a new project or select existing one
3. Copy the connection string from the dashboard
4. Replace the placeholder in `.env`

**BETTER_AUTH_SECRET**:
- Use the same secret configured in Better Auth
- Must be a strong, random string (at least 32 characters)
- Never commit this to version control

### 5. Create Database Tables

Run the migration to create the `tasks` table:

```bash
# Using Alembic (if configured)
alembic upgrade head

# Or run SQL directly
psql $DATABASE_URL < specs/001-task-crud/migrations/001_create_tasks_table.sql
```

**Manual SQL Migration**:
```sql
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
```

### 6. Start Backend Server

```bash
uvicorn main:app --reload --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 7. Verify Backend is Running

Open http://localhost:8000/docs in your browser to see the interactive API documentation (Swagger UI).

## Frontend Setup

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

**Key Dependencies**:
- Next.js 14+
- TypeScript 5.x
- Tailwind CSS 3.x
- Better Auth (for authentication)
- Zod (for validation)

### 3. Configure Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
# API endpoint
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth configuration (if needed)
BETTER_AUTH_SECRET=your-secret-key-here
```

### 4. Start Frontend Development Server

```bash
npm run dev
```

**Expected Output**:
```
▲ Next.js 14.0.0
- Local:        http://localhost:3000
- Ready in 2.3s
```

### 5. Verify Frontend is Running

Open http://localhost:3000 in your browser to see the application.

## Development Workflow

### 1. Implement Backend Endpoints

**File**: `backend/routes/tasks.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID
from typing import List

from models import Task
from schemas import TaskCreate, TaskUpdate, TaskRead, TaskListResponse
from db import get_session
from auth import get_current_user

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    user_id: UUID,
    page: int = 1,
    page_size: int = 20,
    session: Session = Depends(get_session),
    current_user: UUID = Depends(get_current_user)
):
    # Verify user_id matches authenticated user
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Query tasks with pagination
    offset = (page - 1) * page_size
    statement = select(Task).where(Task.user_id == user_id).offset(offset).limit(page_size)
    tasks = session.exec(statement).all()

    # Count total tasks
    count_statement = select(func.count(Task.id)).where(Task.user_id == user_id)
    total = session.exec(count_statement).one()

    return TaskListResponse(
        items=tasks,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )
```

### 2. Implement Frontend Components

**File**: `frontend/components/TaskList.tsx`

```typescript
'use client';

import { useEffect, useState } from 'react';
import { Task } from '@/lib/types';
import { api } from '@/lib/api';

export default function TaskList({ userId }: { userId: string }) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchTasks() {
      try {
        const response = await api.getTasks(userId);
        setTasks(response.items);
      } catch (err) {
        setError('Failed to load tasks');
      } finally {
        setLoading(false);
      }
    }

    fetchTasks();
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="space-y-4">
      {tasks.map(task => (
        <div key={task.id} className="p-4 border rounded">
          <h3 className="font-bold">{task.title}</h3>
          <p className="text-gray-600">{task.description}</p>
          <span className="text-sm text-gray-500">{task.status}</span>
        </div>
      ))}
    </div>
  );
}
```

### 3. Test the Implementation

**Backend Tests** (`backend/tests/test_tasks.py`):
```bash
pytest tests/test_tasks.py -v
```

**Frontend Tests** (`frontend/tests/tasks.test.tsx`):
```bash
npm test
```

## API Testing

### Using cURL

**Create Task**:
```bash
curl -X POST http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

**List Tasks**:
```bash
curl http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Update Task**:
```bash
curl -X PUT http://localhost:8000/api/{user_id}/tasks/{task_id} \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries and supplies", "status": "in_progress"}'
```

**Delete Task**:
```bash
curl -X DELETE http://localhost:8000/api/{user_id}/tasks/{task_id} \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Using Swagger UI

1. Open http://localhost:8000/docs
2. Click "Authorize" button
3. Enter JWT token: `Bearer YOUR_JWT_TOKEN`
4. Try out the endpoints interactively

## Common Issues & Solutions

### Issue: Database Connection Error

**Error**: `could not connect to server: Connection refused`

**Solution**:
1. Verify PostgreSQL is running
2. Check DATABASE_URL in `.env`
3. Ensure firewall allows connection
4. For Neon, verify IP whitelist settings

### Issue: JWT Verification Failed

**Error**: `401 Unauthorized: Invalid token`

**Solution**:
1. Verify BETTER_AUTH_SECRET matches between frontend and backend
2. Check token expiration (tokens expire after 1 hour by default)
3. Ensure Authorization header format: `Bearer <token>`

### Issue: CORS Error

**Error**: `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**:
1. Verify CORS_ORIGINS in backend `.env` includes `http://localhost:3000`
2. Check CORS middleware configuration in `main.py`
3. Restart backend server after changing CORS settings

### Issue: User ID Mismatch

**Error**: `403 Forbidden: You do not have permission to access this resource`

**Solution**:
1. Verify user_id in URL path matches authenticated user's ID from JWT
2. Check JWT token contains correct user_id claim
3. Ensure frontend is passing correct user_id to API calls

## Next Steps

After completing the setup:

1. **Run Tests**: Verify all tests pass
2. **Review API Contract**: Check OpenAPI spec at `/docs`
3. **Implement Frontend Pages**: Create task list and task detail pages
4. **Add Error Handling**: Implement comprehensive error handling
5. **Add Loading States**: Implement loading indicators
6. **Test Authentication**: Verify JWT authentication works end-to-end
7. **Test Data Isolation**: Verify users can only access their own tasks

## Additional Resources

- **Feature Specification**: [spec.md](./spec.md)
- **Implementation Plan**: [plan.md](./plan.md)
- **Data Model**: [data-model.md](./data-model.md)
- **API Contract**: [contracts/tasks-api.yaml](./contracts/tasks-api.yaml)
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Next.js Documentation**: https://nextjs.org/docs
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com

## Support

For questions or issues:
1. Check the specification documents in `specs/001-task-crud/`
2. Review the constitution at `.specify/memory/constitution.md`
3. Consult the project CLAUDE.md files for development guidelines
