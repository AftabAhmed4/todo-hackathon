# Implementation Plan: Task CRUD Operations

**Branch**: `001-task-crud` | **Date**: 2026-01-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-task-crud/spec.md`

## Summary

Implement full CRUD (Create, Read, Update, Delete) operations for user-owned tasks in a full-stack web application. Users can create, view, update, and delete their personal tasks with strict data isolation enforced at the database level. All operations require JWT authentication and are scoped to the authenticated user.

**Technical Approach**: FastAPI backend with SQLModel ORM for PostgreSQL database, Next.js frontend with TypeScript, JWT-based authentication via Better Auth, RESTful API with user-scoped endpoints.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend), Node.js 18+ (frontend runtime)
**Primary Dependencies**: FastAPI 0.104+, SQLModel 0.0.14, Next.js 14+ (App Router), Better Auth (JWT), Tailwind CSS
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (Linux server backend, browser frontend)
**Project Type**: Web (monorepo with frontend/ and backend/ folders)
**Performance Goals**: <2s task list retrieval, <5s task creation, support 100+ concurrent users
**Constraints**: <200ms API response time (p95), strict user data isolation, JWT token validation on all endpoints
**Scale/Scope**: Support 1000+ users, 1000+ tasks per user, paginated responses (20 items/page)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Required Gate Verification

- [x] **Spec-Driven Workflow**: Feature implementation will follow Spec-Kit Plus → Claude Code → Tasks → Implementation workflow. No manual coding.
- [x] **Database Isolation**: All database operations use SQLModel with user-scoped queries via foreign key. No direct frontend-to-database access.
- [x] **JWT Authentication**: All API endpoints secured with JWT tokens. Better Auth issues tokens, backend verifies using BETTER_AUTH_SECRET.
- [x] **API Contract**: Endpoints match defined contract (/api/{user_id}/tasks/*). No divergence from specified paths.
- [x] **Frontend Auth State**: Frontend handles auth state, API client automatically attaches JWT tokens. UI reflects only authenticated user data.
- [x] **Monorepo Structure**: Implementation fits in frontend/ and backend/ folders. Spec-Kit files at root or /specs.
- [x] **No Hardcoded Secrets**: All secrets and DB URLs via environment variables. No hardcoded values in code.
- [x] **Production Quality**: Code is reviewable, production-grade. No placeholder logic, mock auth, or insecure shortcuts.

### Complexity Tracking Justification

No violations. All requirements align with constitution principles.

## Project Structure

### Documentation (this feature)

```text
specs/001-task-crud/
├── spec.md              # Feature specification
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Technical decisions and rationale
├── data-model.md        # Phase 1: Database schema and entity design
├── quickstart.md        # Phase 1: Developer setup guide
├── contracts/           # Phase 1: API contracts (OpenAPI)
│   └── tasks-api.yaml
└── tasks.md             # Phase 2: Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── models.py            # SQLModel Task and User models
├── schemas.py           # Pydantic request/response schemas
├── routes/
│   └── tasks.py         # Task CRUD endpoints
├── auth.py              # JWT verification middleware
├── db.py                # Database connection and session
├── main.py              # FastAPI app entry point
└── tests/
    ├── test_tasks.py    # Task CRUD tests
    └── conftest.py      # Test fixtures

frontend/
├── app/
│   ├── tasks/
│   │   ├── page.tsx     # Task list page
│   │   └── [id]/
│   │       └── page.tsx # Task detail/edit page
│   └── layout.tsx       # Root layout with auth
├── components/
│   ├── TaskList.tsx     # Task list component
│   ├── TaskForm.tsx     # Create/edit task form
│   └── TaskItem.tsx     # Individual task display
├── lib/
│   ├── api.ts           # API client with JWT attachment
│   └── types.ts         # TypeScript types
└── tests/
    └── tasks.test.tsx   # Component tests
```

**Structure Decision**: Web application (Option 2) with separate backend/ and frontend/ folders in monorepo structure. Backend uses FastAPI with modular routes, frontend uses Next.js App Router with component-based architecture.

## Phase 0: Research & Technical Decisions

See [research.md](./research.md) for detailed technical decisions and rationale.

**Key Decisions**:
1. **Database Schema**: Single `tasks` table with foreign key to `users` table, indexed on `user_id`
2. **Authentication Flow**: Better Auth issues JWT → Frontend stores in httpOnly cookie → Backend verifies with BETTER_AUTH_SECRET
3. **API Design**: RESTful endpoints with user_id in path, validated against JWT claims
4. **Pagination**: Offset-based pagination with query parameters (page, page_size)
5. **Error Handling**: Standard HTTP status codes with JSON error responses
6. **Validation**: Pydantic models (backend), Zod schemas (frontend)

## Phase 1: Design Artifacts

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Task Entity**:
- `id`: UUID (primary key)
- `user_id`: UUID (foreign key to users.id, indexed)
- `title`: String (max 500 chars, required)
- `description`: String (max 2000 chars, optional)
- `status`: Enum (pending, in_progress, completed)
- `created_at`: Timestamp (auto-generated)
- `updated_at`: Timestamp (auto-updated)

**Relationships**: Task belongs to User (many-to-one)

### API Contracts

See [contracts/tasks-api.yaml](./contracts/tasks-api.yaml) for OpenAPI specification.

**Endpoints**:
- `GET /api/{user_id}/tasks` - List user's tasks (paginated)
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get single task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task

**Authentication**: All endpoints require `Authorization: Bearer <jwt_token>` header

### Developer Quickstart

See [quickstart.md](./quickstart.md) for setup instructions.

## Implementation Phases

### Phase 2: Task Generation (via /sp.tasks)

Tasks will be generated in dependency order:
1. Backend: Database models and migrations
2. Backend: Authentication middleware
3. Backend: Task CRUD endpoints
4. Backend: Tests
5. Frontend: API client setup
6. Frontend: Task components
7. Frontend: Task pages
8. Frontend: Tests
9. Integration testing
10. Documentation

### Phase 3: Implementation (via /sp.implement)

Automated implementation following generated tasks with validation at each step.

## Security Considerations

1. **JWT Verification**: All endpoints verify JWT signature using BETTER_AUTH_SECRET
2. **User ID Validation**: Path parameter `{user_id}` must match JWT claims
3. **Data Isolation**: All queries filter by authenticated user_id
4. **Input Validation**: Pydantic models validate all inputs
5. **SQL Injection Prevention**: SQLModel ORM prevents SQL injection
6. **XSS Prevention**: Frontend sanitizes user input
7. **Rate Limiting**: Consider implementing rate limiting for task creation

## Performance Optimizations

1. **Database Indexing**: Index on `tasks.user_id` for fast user-scoped queries
2. **Pagination**: Limit query results to 20 items per page
3. **Connection Pooling**: Use SQLModel async sessions with connection pooling
4. **Caching**: Consider Redis caching for frequently accessed tasks
5. **Query Optimization**: Use SQLModel select() with specific columns when needed

## Testing Strategy

1. **Unit Tests**: Test individual functions and components
2. **Integration Tests**: Test API endpoints with test database
3. **Contract Tests**: Validate API responses match OpenAPI spec
4. **E2E Tests**: Test complete user flows (create → read → update → delete)
5. **Security Tests**: Verify authentication and authorization enforcement

## Deployment Considerations

1. **Environment Variables**: DATABASE_URL, BETTER_AUTH_SECRET, API_PORT, NEXT_PUBLIC_API_URL
2. **Database Migrations**: Use Alembic for schema migrations
3. **CORS Configuration**: Configure CORS for frontend-backend communication
4. **Health Checks**: Implement /health endpoint for monitoring
5. **Logging**: Structured logging for debugging and audit trail

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| JWT token expiration during operation | User session interrupted | Implement token refresh mechanism |
| Database connection pool exhaustion | API requests fail | Configure appropriate pool size and timeouts |
| Pagination performance with large datasets | Slow queries | Use cursor-based pagination for large datasets |
| Concurrent updates to same task | Data inconsistency | Implement optimistic locking with version field |

## Success Metrics

- All 18 functional requirements implemented and tested
- All 8 success criteria met (response times, data isolation, error handling)
- 100% test coverage for critical paths (CRUD operations, authentication)
- Zero security vulnerabilities (SQL injection, XSS, unauthorized access)
- Production-ready code with comprehensive error handling and logging
