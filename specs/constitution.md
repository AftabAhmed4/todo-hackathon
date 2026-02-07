# Todo Full-Stack Web Application - Project Constitution (Phase II)

**Version**: 2.0.0
**Ratified**: 2026-01-09
**Last Amended**: 2026-01-09
**Phase**: Hackathon II - Production-Grade Full-Stack Implementation

---

## I. Project Identity & Vision

### Project Name
**Todo Full-Stack Web Application (Phase II)**

### Purpose
Build a production-grade, secure, multi-user todo application demonstrating:
- Spec-driven agentic development workflow
- Enterprise-level authentication and data isolation
- Modern full-stack architecture with Next.js and FastAPI
- Hackathon-ready code quality suitable for judge evaluation

### Vision Statement
Deliver a fully functional, secure, and scalable todo application that showcases best practices in:
- **Security**: JWT-based authentication with strict user data isolation
- **Architecture**: Clean separation of concerns across frontend and backend
- **Development Process**: Spec-first approach with AI-assisted implementation
- **Code Quality**: Production-ready code with comprehensive error handling

### Success Criteria
- All API endpoints secured with JWT authentication
- Zero cross-user data leakage (strict tenant isolation)
- Responsive, modern UI with graceful error states
- Deployable to production without modifications
- Code passes hackathon judge review standards

---

## II. Non-Negotiable Development Rules

### Rule 1: Spec-First Development (ABSOLUTE)
**ALL development MUST follow this workflow:**
1. Write specification in `/specs/` directory
2. Generate implementation plan via Spec-Kit Plus
3. Generate tasks from plan
4. Implement via Claude Code (no manual coding)

**Violations**: Any code written without a corresponding spec is REJECTED.

**Rationale**: Ensures traceability, prevents scope creep, and maintains documentation-code alignment for judge review.

### Rule 2: Zero Manual Coding (ABSOLUTE)
**ALL code MUST be generated via Claude Code following specs.**

No developer may write code manually. All implementation must be AI-assisted following the spec-driven workflow.

**Rationale**: Demonstrates agentic development capabilities and ensures consistency with specifications.

### Rule 3: JWT Required for ALL APIs (ABSOLUTE)
**EVERY API endpoint MUST:**
- Require `Authorization: Bearer <token>` header
- Verify JWT signature using `BETTER_AUTH_SECRET`
- Extract user ID from verified token
- Scope all data operations to authenticated user

**Violations**: Any endpoint accessible without valid JWT is a CRITICAL SECURITY FAILURE.

**Rationale**: Stateless authentication enables horizontal scaling and prevents unauthorized access.

### Rule 4: User Data Isolation (ABSOLUTE)
**ALL database queries MUST:**
- Filter by authenticated user ID via foreign key
- Use SQLModel ORM exclusively (no raw SQL)
- Prevent cross-user data access at database level
- Enforce ownership validation in all CRUD operations

**Violations**: Any query returning another user's data is a CRITICAL SECURITY FAILURE.

**Rationale**: Guarantees multi-tenant data isolation and prevents data leakage.

### Rule 5: No Hardcoded Secrets (ABSOLUTE)
**ALL secrets MUST:**
- Be stored in environment variables
- Never appear in source code
- Never be committed to version control
- Be documented in `.env.example` (without values)

**Violations**: Any hardcoded secret results in immediate rejection.

**Rationale**: Prevents credential leakage and enables secure deployment across environments.

### Rule 6: Production Quality Only (ABSOLUTE)
**ALL code MUST be:**
- Production-ready (no placeholders, no TODOs)
- Fully error-handled with appropriate HTTP status codes
- Logged for debugging and monitoring
- Modular and reusable
- Testable and reviewable

**Violations**: Placeholder logic, mock authentication, or insecure shortcuts are REJECTED.

**Rationale**: Hackathon judges evaluate production readiness, not prototypes.

---

## III. Locked Technology Stack

### Frontend Stack (NON-NEGOTIABLE)
- **Framework**: Next.js 16+ (App Router only)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth (client-side JWT handling)
- **State Management**: React hooks + Context API
- **HTTP Client**: Fetch API with custom wrapper in `/lib/api.ts`

**Constraints**:
- Server components by default
- Client components only for interactivity
- No direct database access from frontend
- All API calls through centralized client

### Backend Stack (NON-NEGOTIABLE)
- **Framework**: Python FastAPI
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT verification (stateless)
- **Validation**: Pydantic models
- **Error Handling**: HTTPException with proper status codes

**Constraints**:
- All routes under `/api/` prefix
- JSON responses only
- No session storage (stateless)
- Environment-based configuration

### Authentication Stack (NON-NEGOTIABLE)
- **Provider**: Better Auth
- **Token Type**: JWT (JSON Web Tokens)
- **Token Delivery**: `Authorization: Bearer <token>` header
- **Token Verification**: Shared secret (`BETTER_AUTH_SECRET`)
- **Token Claims**: Must include `user_id` for data scoping

**Security Requirements**:
- HTTPS in production
- Secure token storage (httpOnly cookies or secure localStorage)
- Token expiration and refresh
- No token in URL parameters

### Database Stack (NON-NEGOTIABLE)
- **Provider**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Schema**: User-owned tasks with foreign key constraints
- **Migrations**: Alembic (if needed)

**Data Model Requirements**:
```sql
users table:
  - id (primary key)
  - email (unique)
  - created_at

tasks table:
  - id (primary key)
  - user_id (foreign key to users.id, NOT NULL)
  - title (string, NOT NULL)
  - description (text, nullable)
  - completed (boolean, default false)
  - created_at (timestamp)
  - updated_at (timestamp)
```

---

## IV. System Architecture Overview

### Monorepo Structure
```
hackathon-todo/
├── frontend/              # Next.js 16 application
│   ├── app/              # App Router pages
│   ├── components/       # Reusable UI components
│   ├── lib/              # API client, utilities
│   └── CLAUDE.md         # Frontend development guidelines
├── backend/              # FastAPI application
│   ├── main.py           # FastAPI entry point
│   ├── models.py         # SQLModel database models
│   ├── routes/           # API route handlers
│   ├── db.py             # Database connection
│   └── CLAUDE.md         # Backend development guidelines
├── specs/                # Feature specifications
│   ├── constitution.md   # This file
│   ├── overview.md       # Project overview
│   └── features/         # Feature-specific specs
├── .specify/             # Spec-Kit Plus artifacts
│   ├── memory/           # Constitution and context
│   └── templates/        # Spec, plan, task templates
└── CLAUDE.md             # Root development guidelines
```

### Communication Flow
```
User Browser
    ↓ (HTTPS)
Next.js Frontend (Port 3000)
    ↓ (HTTP + JWT in Authorization header)
FastAPI Backend (Port 8000)
    ↓ (SQLModel ORM)
Neon PostgreSQL Database
```

### Authentication Flow
```
1. User submits credentials → Better Auth
2. Better Auth validates → Issues JWT token
3. Frontend stores token → Attaches to all API requests
4. Backend verifies JWT → Extracts user_id
5. Backend queries database → Filters by user_id
6. Backend returns response → Only user's data
```

---

## V. Authentication Constitution

### Better Auth Integration (Frontend)
**Responsibilities**:
- Handle user registration and login UI
- Store JWT tokens securely
- Attach tokens to all API requests automatically
- Handle token expiration and refresh
- Redirect unauthenticated users to login

**Implementation Requirements**:
- Better Auth SDK configured in `/lib/auth.ts`
- Token stored in httpOnly cookies (preferred) or secure localStorage
- API client in `/lib/api.ts` automatically includes token
- Auth context provider wraps application
- Protected routes check authentication state

### JWT Verification (Backend)
**Responsibilities**:
- Verify JWT signature on every request
- Extract user_id from verified token
- Reject invalid or expired tokens
- Return 401 Unauthorized for missing/invalid tokens
- Scope all database operations to authenticated user

**Implementation Requirements**:
- JWT verification middleware in `backend/auth.py`
- Shared secret from `BETTER_AUTH_SECRET` environment variable
- Dependency injection for authenticated user context
- All route handlers receive authenticated user_id
- No endpoint bypasses authentication

### Security Guarantees
- **Stateless**: No server-side session storage
- **Scalable**: Tokens verified independently on each request
- **Secure**: Tokens signed with secret, cannot be forged
- **Scoped**: Every request tied to specific user_id
- **Auditable**: All operations logged with user context

---

## VI. REST API Constitution

### Endpoint Contract (IMMUTABLE)
**ALL endpoints MUST follow this exact contract:**

```
GET    /api/{user_id}/tasks           # List all tasks for user
POST   /api/{user_id}/tasks           # Create new task for user
GET    /api/{user_id}/tasks/{id}      # Get specific task
PUT    /api/{user_id}/tasks/{id}      # Update specific task
DELETE /api/{user_id}/tasks/{id}      # Delete specific task
PATCH  /api/{user_id}/tasks/{id}/complete  # Toggle task completion
```

**Path Parameter Validation**:
- `{user_id}` in URL MUST match authenticated user's ID from JWT
- Requests with mismatched user_id MUST return 403 Forbidden
- `{id}` MUST be validated to belong to authenticated user

### Request/Response Standards
**Request Format**:
```json
POST /api/{user_id}/tasks
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Task title (required)",
  "description": "Task description (optional)"
}
```

**Success Response**:
```json
HTTP 200 OK / 201 Created
Content-Type: application/json

{
  "id": 123,
  "user_id": 456,
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-01-09T12:00:00Z",
  "updated_at": "2026-01-09T12:00:00Z"
}
```

**Error Response**:
```json
HTTP 4xx / 5xx
Content-Type: application/json

{
  "detail": "Human-readable error message"
}
```

### HTTP Status Codes (REQUIRED)
- **200 OK**: Successful GET, PUT, PATCH, DELETE
- **201 Created**: Successful POST
- **400 Bad Request**: Invalid request body or parameters
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: Valid token but insufficient permissions
- **404 Not Found**: Resource does not exist or not owned by user
- **500 Internal Server Error**: Unexpected server error

### Security Enforcement
**EVERY endpoint MUST:**
1. Verify JWT token presence and validity
2. Extract user_id from token
3. Validate path `{user_id}` matches token user_id
4. Filter database queries by authenticated user_id
5. Return 404 (not 403) for resources owned by other users (prevents enumeration)
6. Log all access attempts with user context

---

## VII. Database Constitution

### Schema Requirements
**Users Table**:
```python
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Tasks Table**:
```python
class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    title: str = Field(nullable=False)
    description: str | None = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Ownership Rules (ABSOLUTE)
**ALL database operations MUST:**
1. Use SQLModel ORM (no raw SQL)
2. Filter by `user_id` in WHERE clause
3. Validate ownership before updates/deletes
4. Use foreign key constraints for referential integrity
5. Index `user_id` for query performance

**Example Query Pattern**:
```python
# CORRECT: Filtered by authenticated user
task = session.exec(
    select(Task)
    .where(Task.id == task_id)
    .where(Task.user_id == authenticated_user_id)
).first()

# INCORRECT: No user filter (SECURITY VIOLATION)
task = session.exec(select(Task).where(Task.id == task_id)).first()
```

### Data Isolation Guarantees
- **No shared tasks**: Every task belongs to exactly one user
- **No global queries**: All queries scoped to authenticated user
- **No cross-user access**: Database constraints prevent data leakage
- **Audit trail**: All operations logged with user context

---

## VIII. Frontend Constitution

### Next.js Responsibilities
**Frontend MUST handle:**
1. User authentication state management
2. JWT token storage and attachment
3. Responsive UI rendering
4. Client-side validation
5. Error state display
6. Loading state display
7. Optimistic UI updates (optional)

### Component Architecture
**Structure**:
```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with auth provider
│   ├── page.tsx            # Landing/dashboard page
│   ├── login/page.tsx      # Login page
│   └── tasks/page.tsx      # Tasks list page
├── components/
│   ├── TaskList.tsx        # Task list component
│   ├── TaskItem.tsx        # Individual task component
│   ├── TaskForm.tsx        # Task creation/edit form
│   └── AuthGuard.tsx       # Protected route wrapper
└── lib/
    ├── api.ts              # API client with JWT handling
    ├── auth.ts             # Better Auth configuration
    └── types.ts            # TypeScript type definitions
```

### API Client Pattern
**ALL backend calls MUST use centralized client**:
```typescript
// lib/api.ts
export const api = {
  async getTasks(userId: number): Promise<Task[]> {
    const token = getAuthToken(); // From Better Auth
    const response = await fetch(`${API_URL}/api/${userId}/tasks`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    if (!response.ok) throw new Error('Failed to fetch tasks');
    return response.json();
  },
  // ... other methods
};
```

### UI/UX Requirements
- **Responsive**: Mobile-first design, works on all screen sizes
- **Accessible**: Semantic HTML, ARIA labels, keyboard navigation
- **Error Handling**: User-friendly error messages, retry options
- **Loading States**: Skeletons or spinners during async operations
- **Validation**: Client-side validation before API calls
- **Feedback**: Success/error toasts or notifications

---

## IX. Backend Constitution

### FastAPI Responsibilities
**Backend MUST handle:**
1. JWT token verification on every request
2. User ID extraction from verified token
3. Database query execution with user scoping
4. Request validation via Pydantic models
5. Error handling with appropriate HTTP status codes
6. Logging for debugging and audit

### Route Handler Pattern
**ALL route handlers MUST follow this pattern**:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from .auth import get_current_user
from .db import get_session

router = APIRouter()

@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: int,
    current_user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Validate path user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Query with user scoping
    tasks = session.exec(
        select(Task).where(Task.user_id == current_user_id)
    ).all()

    return tasks
```

### Dependency Injection
**Required dependencies**:
- `get_current_user`: Verifies JWT, returns user_id
- `get_session`: Provides database session
- `validate_ownership`: Ensures resource belongs to user

### Error Handling Standards
**ALL errors MUST be handled**:
```python
try:
    # Database operation
    task = session.exec(query).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
except SQLAlchemyError as e:
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

### Logging Requirements
**ALL operations MUST be logged**:
```python
logger.info(f"User {user_id} fetching tasks")
logger.error(f"Failed to create task for user {user_id}: {error}")
```

---

## X. Agentic Development Workflow

### Spec-Kit Plus Workflow (MANDATORY)
**Phase 0: Specification**
1. Write feature spec in `/specs/features/[feature].md`
2. Define user stories with acceptance criteria
3. Specify functional requirements
4. Document success criteria

**Phase 1: Planning**
1. Run `/sp.plan` to generate implementation plan
2. Review technical approach and architecture
3. Validate constitution compliance
4. Approve plan before implementation

**Phase 2: Task Generation**
1. Run `/sp.tasks` to generate task list
2. Review task breakdown and dependencies
3. Validate task completeness
4. Approve tasks before implementation

**Phase 3: Implementation**
1. Run `/sp.implement` to execute tasks via Claude Code
2. Monitor progress and validate each task
3. Review generated code for quality
4. Test functionality after implementation

**Phase 4: Validation**
1. Verify all acceptance criteria met
2. Test authentication and data isolation
3. Validate API contract compliance
4. Review code for production readiness

### Claude Code Integration
**ALL code generation MUST:**
- Follow specs exactly (no improvisation)
- Use templates from `.specify/templates/`
- Maintain constitution compliance
- Generate production-quality code
- Include comprehensive error handling
- Add appropriate logging

### Quality Gates
**Before merging, verify**:
- [ ] Spec exists and is complete
- [ ] Plan approved and constitution-compliant
- [ ] Tasks generated and reviewed
- [ ] Implementation complete and tested
- [ ] JWT authentication working
- [ ] User data isolation verified
- [ ] API contract followed
- [ ] No hardcoded secrets
- [ ] Production-quality code
- [ ] Error handling comprehensive
- [ ] Logging in place

---

## XI. Hackathon Evaluation Readiness

### Judge Review Criteria
**Judges will evaluate**:
1. **Security**: JWT authentication, data isolation, no vulnerabilities
2. **Architecture**: Clean separation, proper patterns, scalability
3. **Code Quality**: Production-ready, well-structured, maintainable
4. **Documentation**: Clear specs, comprehensive README, inline comments
5. **Functionality**: All features working, no bugs, good UX
6. **Innovation**: Agentic development workflow, spec-driven approach

### Demonstration Checklist
**Prepare to demonstrate**:
- [ ] User registration and login flow
- [ ] JWT token issuance and verification
- [ ] Task CRUD operations (create, read, update, delete)
- [ ] Task completion toggle
- [ ] User data isolation (cannot see other users' tasks)
- [ ] Error handling (invalid token, missing fields, etc.)
- [ ] Responsive UI on mobile and desktop
- [ ] Spec-to-code traceability

### Documentation Requirements
**Must include**:
- [ ] `/specs/constitution.md` (this file)
- [ ] `/specs/overview.md` (project overview)
- [ ] `/specs/features/*.md` (feature specifications)
- [ ] `README.md` (setup instructions, architecture overview)
- [ ] `backend/CLAUDE.md` (backend guidelines)
- [ ] `frontend/CLAUDE.md` (frontend guidelines)
- [ ] `.env.example` (required environment variables)

### Deployment Readiness
**Must be deployable**:
- [ ] Environment variables documented
- [ ] Database migrations ready
- [ ] Frontend builds without errors
- [ ] Backend starts without errors
- [ ] HTTPS configured for production
- [ ] CORS configured properly
- [ ] Error logging configured
- [ ] Health check endpoints available

---

## XII. Amendment Rules

### Version Semantics
- **MAJOR (X.0.0)**: Backward-incompatible changes to core principles or stack
- **MINOR (x.Y.0)**: New principles added or existing principles expanded
- **PATCH (x.y.Z)**: Clarifications, typo fixes, non-semantic changes

### Amendment Procedure
1. **Propose Change**: Document proposed amendment with rationale
2. **Impact Analysis**: Identify affected specs, plans, tasks, and code
3. **Update Constitution**: Increment version, update content
4. **Propagate Changes**: Update dependent templates and documentation
5. **Validate Consistency**: Ensure all references updated
6. **Record Amendment**: Update Sync Impact Report
7. **Commit Changes**: Create commit with amendment details

### Approval Authority
- **MAJOR changes**: Require team consensus and stakeholder approval
- **MINOR changes**: Require technical lead approval
- **PATCH changes**: Can be approved by any team member

### Sync Impact Report
**Every amendment MUST include**:
- Version change (old → new)
- List of modified principles
- Added sections
- Removed sections
- Templates requiring updates
- Follow-up TODOs

---

## XIII. Compliance & Enforcement

### Continuous Compliance
**Every PR MUST verify**:
- [ ] Constitution principles followed
- [ ] Spec-driven workflow used
- [ ] JWT authentication present
- [ ] User data isolation maintained
- [ ] API contract followed
- [ ] No hardcoded secrets
- [ ] Production-quality code
- [ ] Error handling comprehensive

### Violation Handling
**If violation detected**:
1. **Document**: Record violation details and impact
2. **Assess**: Determine severity (critical, major, minor)
3. **Remediate**: Fix violation immediately
4. **Review**: Analyze root cause
5. **Prevent**: Update processes to prevent recurrence

### Audit Trail
**ALL changes MUST be logged**:
- Git commits with descriptive messages
- PR descriptions with constitution compliance checklist
- Code review comments referencing constitution principles
- Deployment logs with validation results

---

## XIV. Core Governance Principles

**Correctness > Convenience**
Never compromise correctness for development speed.

**Security > Speed**
Never compromise security for feature velocity.

**Spec > Assumptions**
Never implement based on assumptions; always follow specs.

**Quality > Quantity**
Never sacrifice code quality for feature count.

**Traceability > Flexibility**
Never implement without spec-to-code traceability.

---

## Appendix A: Quick Reference

### Environment Variables
```bash
# Backend
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=your-secret-key-here
API_PORT=8000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000/api/auth
```

### Development Commands
```bash
# Frontend
cd frontend && npm install && npm run dev

# Backend
cd backend && pip install -r requirements.txt && uvicorn main:app --reload

# Both (Docker)
docker-compose up
```

### API Testing
```bash
# Login (get JWT)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# List tasks (with JWT)
curl -X GET http://localhost:8000/api/123/tasks \
  -H "Authorization: Bearer <jwt_token>"

# Create task (with JWT)
curl -X POST http://localhost:8000/api/123/tasks \
  -H "Authorization: Bearer <jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"New task","description":"Task description"}'
```

---

**END OF CONSTITUTION**

This constitution is the supreme governing document for the Todo Full-Stack Web Application (Phase II). All development decisions, technical choices, and implementation details must align with the principles and requirements defined herein.

**Version**: 2.0.0 | **Ratified**: 2026-01-09 | **Last Amended**: 2026-01-09
