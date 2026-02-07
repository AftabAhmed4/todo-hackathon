# Research & Technical Decisions: Task CRUD Operations

**Feature**: Task CRUD Operations
**Date**: 2026-01-12
**Status**: Complete

## Overview

This document captures technical research, decisions, and rationale for implementing Task CRUD operations in the hackathon todo application.

## Technical Decisions

### 1. Database Schema Design

**Decision**: Single `tasks` table with foreign key to `users` table, indexed on `user_id`

**Rationale**:
- Simple, normalized schema following relational database best practices
- Foreign key constraint ensures referential integrity
- Index on `user_id` enables fast user-scoped queries
- Supports efficient pagination and filtering

**Alternatives Considered**:
- **Separate table per user**: Rejected due to schema management complexity and poor scalability
- **NoSQL document store**: Rejected to maintain consistency with existing PostgreSQL infrastructure
- **Composite primary key (user_id, task_id)**: Rejected in favor of UUID primary key for simpler API design

**Implementation Details**:
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
```

### 2. Authentication Flow

**Decision**: Better Auth issues JWT → Frontend stores in httpOnly cookie → Backend verifies with BETTER_AUTH_SECRET

**Rationale**:
- Stateless authentication scales horizontally without session storage
- JWT contains user_id claim for efficient authorization
- httpOnly cookies prevent XSS attacks
- Shared secret (BETTER_AUTH_SECRET) enables token verification without database lookup

**Alternatives Considered**:
- **Session-based auth**: Rejected due to state management complexity and scaling limitations
- **OAuth2 with external provider**: Rejected as Better Auth is already integrated
- **API keys**: Rejected due to lack of expiration and revocation mechanisms

**Token Structure**:
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234571490
}
```

### 3. API Design Pattern

**Decision**: RESTful endpoints with user_id in path, validated against JWT claims

**Rationale**:
- RESTful design is intuitive and follows HTTP semantics
- user_id in path makes ownership explicit in URL structure
- Path validation against JWT prevents unauthorized access attempts
- Standard HTTP methods (GET, POST, PUT, DELETE) map naturally to CRUD operations

**Alternatives Considered**:
- **GraphQL**: Rejected due to added complexity for simple CRUD operations
- **RPC-style endpoints**: Rejected in favor of REST conventions
- **user_id in query params**: Rejected as path parameters better represent resource hierarchy

**Endpoint Design**:
```
GET    /api/{user_id}/tasks          # List tasks
POST   /api/{user_id}/tasks          # Create task
GET    /api/{user_id}/tasks/{id}     # Get task
PUT    /api/{user_id}/tasks/{id}     # Update task
DELETE /api/{user_id}/tasks/{id}     # Delete task
```

### 4. Pagination Strategy

**Decision**: Offset-based pagination with query parameters (page, page_size)

**Rationale**:
- Simple to implement and understand
- Works well for datasets up to 10,000 items
- Supports random page access (jump to page N)
- Default page size of 20 balances performance and UX

**Alternatives Considered**:
- **Cursor-based pagination**: Rejected for initial implementation (can migrate later if needed)
- **Infinite scroll**: Rejected as it requires cursor-based pagination
- **Load all items**: Rejected due to performance concerns with large datasets

**Implementation**:
```python
# Query parameters
page: int = 1          # Default to first page
page_size: int = 20    # Default 20 items per page

# Response format
{
  "items": [...],
  "total": 150,
  "page": 1,
  "page_size": 20,
  "total_pages": 8
}
```

### 5. Error Handling Strategy

**Decision**: Standard HTTP status codes with JSON error responses

**Rationale**:
- HTTP status codes provide semantic meaning (200, 201, 400, 401, 403, 404, 500)
- JSON error responses enable client-side error handling
- Consistent error format across all endpoints
- User-friendly error messages without exposing internal details

**Error Response Format**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required and cannot be empty",
    "field": "title"
  }
}
```

**Status Code Mapping**:
- 200 OK: Successful GET, PUT, DELETE
- 201 Created: Successful POST
- 400 Bad Request: Validation errors
- 401 Unauthorized: Missing or invalid JWT
- 403 Forbidden: Valid JWT but user_id mismatch
- 404 Not Found: Task doesn't exist or doesn't belong to user
- 500 Internal Server Error: Unexpected server errors

### 6. Input Validation

**Decision**: Pydantic models (backend), Zod schemas (frontend)

**Rationale**:
- Pydantic integrates natively with FastAPI for automatic validation
- Zod provides TypeScript-first schema validation
- Both libraries support complex validation rules
- Validation errors are automatically formatted and returned

**Backend Validation (Pydantic)**:
```python
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=2000)
    status: TaskStatus = TaskStatus.PENDING
```

**Frontend Validation (Zod)**:
```typescript
const taskSchema = z.object({
  title: z.string().min(1).max(500),
  description: z.string().max(2000).optional(),
  status: z.enum(['pending', 'in_progress', 'completed'])
});
```

### 7. Database Connection Management

**Decision**: SQLModel async sessions with connection pooling

**Rationale**:
- Async operations prevent blocking during I/O
- Connection pooling reduces overhead of creating new connections
- SQLModel provides type-safe ORM with Pydantic integration
- Automatic session cleanup prevents connection leaks

**Configuration**:
```python
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### 8. CORS Configuration

**Decision**: Configure CORS to allow frontend origin with credentials

**Rationale**:
- Frontend and backend run on different ports during development
- Credentials (cookies) must be allowed for JWT transmission
- Restrict allowed origins to prevent unauthorized access

**Configuration**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

## Best Practices Applied

### Backend (FastAPI + SQLModel)

1. **Dependency Injection**: Use FastAPI dependencies for database sessions and auth
2. **Type Safety**: Leverage Pydantic models for request/response validation
3. **Error Handling**: Centralized exception handlers for consistent error responses
4. **Logging**: Structured logging with request IDs for debugging
5. **Testing**: pytest with test database fixtures

### Frontend (Next.js + TypeScript)

1. **Type Safety**: TypeScript strict mode with proper type definitions
2. **Component Structure**: Reusable components with clear props interfaces
3. **State Management**: React hooks for local state, API client for server state
4. **Error Boundaries**: Graceful error handling with user-friendly messages
5. **Loading States**: Skeleton loaders and loading indicators

### Security

1. **JWT Verification**: Verify signature and expiration on every request
2. **User ID Validation**: Ensure path user_id matches JWT claims
3. **SQL Injection Prevention**: Use ORM parameterized queries
4. **XSS Prevention**: Sanitize user input on frontend
5. **HTTPS Only**: Enforce HTTPS in production

## Performance Considerations

1. **Database Indexing**: Index on user_id and status columns
2. **Query Optimization**: Select only needed columns, avoid N+1 queries
3. **Pagination**: Limit result sets to 20 items per page
4. **Connection Pooling**: Reuse database connections
5. **Caching**: Consider Redis for frequently accessed data (future enhancement)

## Testing Strategy

1. **Unit Tests**: Test individual functions and components in isolation
2. **Integration Tests**: Test API endpoints with test database
3. **Contract Tests**: Validate API responses match OpenAPI specification
4. **E2E Tests**: Test complete user flows from frontend to backend
5. **Security Tests**: Verify authentication and authorization enforcement

## Migration Path

### Phase 1: Initial Implementation
- Basic CRUD operations
- JWT authentication
- Offset-based pagination

### Phase 2: Enhancements (Future)
- Cursor-based pagination for large datasets
- Redis caching for performance
- Full-text search on task titles/descriptions
- Task filtering and sorting options
- Bulk operations (delete multiple tasks)

## Dependencies

### Backend
- FastAPI 0.104+
- SQLModel 0.0.14
- python-jose[cryptography] 3.3.0 (JWT verification)
- passlib[bcrypt] 1.7.4 (password hashing)
- psycopg2-binary 2.9.9 (PostgreSQL driver)
- pytest 7.4+ (testing)

### Frontend
- Next.js 14+ (App Router)
- TypeScript 5.x
- Tailwind CSS 3.x
- Zod 3.x (validation)
- React Hook Form 7.x (form handling)
- Jest + React Testing Library (testing)

## Conclusion

All technical decisions align with the project constitution and support the functional requirements defined in the specification. The chosen architecture provides a solid foundation for implementing Task CRUD operations with proper security, performance, and maintainability.
