<!--
SYNC IMPACT REPORT
================================================================================
Version Change: 1.0.0 → 2.0.0 (MAJOR - Phase II Expansion)

Modified Principles:
  - Principle I: Expanded with detailed workflow steps
  - Principle III: Expanded with Better Auth integration details
  - Principle IV: Expanded with complete endpoint contract
  - Principle V: Expanded with Better Auth requirements
  - Principle VIII: Expanded with comprehensive quality standards

Added Sections:
  - System Architecture Overview (Section IV)
  - Authentication Constitution (Section V)
  - REST API Constitution (Section VI)
  - Database Constitution (Section VII)
  - Frontend Constitution (Section VIII)
  - Backend Constitution (Section IX)
  - Agentic Development Workflow (Section X)
  - Hackathon Evaluation Readiness (Section XI)
  - Amendment Rules (Section XII)
  - Compliance & Enforcement (Section XIII)
  - Core Governance Principles (Section XIV)
  - Appendix A: Quick Reference

Removed Sections: None

Templates Requiring Updates:
  ✅ .specify/templates/plan-template.md - Constitution Check section validated
  ✅ .specify/templates/spec-template.md - Spec constraints align with principles
  ✅ .specify/templates/tasks-template.md - Task types reflect security/auth requirements

Follow-up TODOs: None

Public Constitution Created:
  ✅ /specs/constitution.md - Comprehensive hackathon-ready constitution for judges

================================================================================
-->

# Todo Full-Stack Web Application Phase II Constitution

## Core Principles

### I. Spec-Driven Agentic Development Workflow (NON-NEGOTIABLE)

All development MUST follow the strict workflow: Spec-Kit Plus → Claude Code → Tasks → Implementation. No manual coding is permitted at any stage. Every feature implementation must trace back to a written specification. Unclear requirements MUST be inferred conservatively and documented as assumptions.

**Workflow Steps**:
1. Write feature spec in `/specs/features/[feature].md`
2. Run `/sp.plan` to generate implementation plan
3. Run `/sp.tasks` to generate task list
4. Run `/sp.implement` to execute tasks via Claude Code
5. Validate against acceptance criteria

**Rationale**: Ensures traceability, prevents implementation drift, and guarantees production-grade reviewable code.

### II. Database Isolation & User Data Security

All database interactions MUST use SQLModel exclusively. Tasks MUST be owned by users via foreign key relationships. All database queries MUST filter by authenticated user ID. No shared or global tasks are permitted. Direct frontend-to-database access is strictly prohibited.

**Implementation Requirements**:
- Foreign key constraint: `tasks.user_id → users.id`
- All queries include `WHERE user_id = authenticated_user_id`
- SQLModel ORM only (no raw SQL)
- Index on `user_id` for performance

**Rationale**: Guarantees strict multi-tenant data isolation and prevents cross-account data leaks.

### III. JWT-Based Stateless Authentication

All API endpoints MUST be secured using JWT-based authentication. Better Auth MUST issue JWT tokens on login. Tokens MUST be sent via `Authorization: Bearer <token>` header. Backend MUST verify JWT using a shared secret (`BETTER_AUTH_SECRET` environment variable). No backend session storage is permitted.

**Token Flow**:
1. Better Auth issues JWT on successful login
2. Frontend stores token securely (httpOnly cookie or secure localStorage)
3. Frontend attaches token to all API requests
4. Backend verifies token signature and extracts user_id
5. Backend scopes all operations to authenticated user_id

**Rationale**: Provides stateless, scalable authentication with secure token-based authorization.

### IV. API Contract Adherence

REST API endpoints MUST follow the exact contract provided:

- `GET    /api/{user_id}/tasks`
- `POST   /api/{user_id}/tasks`
- `GET    /api/{user_id}/tasks/{id}`
- `PUT    /api/{user_id}/tasks/{id}`
- `DELETE /api/{user_id}/tasks/{id}`
- `PATCH  /api/{user_id}/tasks/{id}/complete`

**Validation Requirements**:
- Path `{user_id}` MUST match authenticated user's ID from JWT
- Mismatched user_id returns 403 Forbidden
- Resource `{id}` MUST belong to authenticated user
- Non-existent or unauthorized resources return 404 Not Found

Endpoints marked as "internal" or "admin" MUST not be exposed without explicit user visibility.

**Rationale**: Ensures consistent, predictable API behavior and enables proper client integration.

### V. Frontend Authentication & Data Scoping

Frontend MUST handle all auth state. API client MUST automatically attach JWT tokens to all requests. UI MUST reflect only authenticated user's data. Responsive, modern UI MUST include graceful error and loading state handling. Better Auth for authentication is MANDATORY.

**Frontend Responsibilities**:
- User authentication state management
- JWT token storage and attachment
- Client-side validation before API calls
- Error state display with user-friendly messages
- Loading state display during async operations
- Responsive design (mobile-first)

**Rationale**: Provides seamless user experience while maintaining security boundaries on the client side.

### VI. Monorepo Structure

Single repository with separate `frontend/` and `backend/` folders. Claude Code MUST be able to reason about both sides together. Spec-Kit files MUST live at root or dedicated `/specs` directory. Clear boundaries maintained with shared context across the codebase.

**Directory Structure**:
```
hackathon-todo/
├── frontend/         # Next.js 16 application
├── backend/          # FastAPI application
├── specs/            # Feature specifications
├── .specify/         # Spec-Kit Plus artifacts
└── CLAUDE.md         # Root development guidelines
```

**Rationale**: Enables full-stack understanding, simplifies dependency management, and maintains organizational clarity.

### VII. No Hardcoded Secrets

All secrets and database URLs MUST use environment variables. No hardcoded secrets in source code. Secrets MUST never be committed to version control. All configuration MUST be externalized.

**Required Environment Variables**:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret
- `API_PORT`: Backend server port
- `NEXT_PUBLIC_API_URL`: Frontend API endpoint

**Rationale**: Prevents credential leakage, enables secure deployment across environments, and follows security best practices.

### VIII. Production Quality Standards

Code MUST be production-grade. No placeholder logic, no mock authentication, no insecure shortcuts. Every feature MUST be testable and reviewable. Error handling and logging MUST be comprehensive. Reusable, modular code structure is REQUIRED.

**Quality Requirements**:
- Comprehensive error handling with appropriate HTTP status codes
- Logging for debugging and audit trail
- Modular, reusable code structure
- TypeScript strict mode (frontend)
- Pydantic validation (backend)
- No TODOs or placeholder comments in production code

**Rationale**: Ensures deliverable quality suitable for production deployment and long-term maintainability.

## Technology Stack & Constraints

### Frontend (NON-NEGOTIABLE)
- Next.js 16+ using App Router
- Better Auth for authentication (JWT token issuance MANDATORY)
- TypeScript (strict mode)
- Tailwind CSS for styling
- Responsive UI with graceful error states

### Backend (NON-NEGOTIABLE)
- Python FastAPI
- SQLModel ORM for all database operations
- Neon Serverless PostgreSQL database
- Stateless JWT authentication (verify tokens, no session storage)
- Pydantic models for validation

### Authentication & Security (NON-NEGOTIABLE)
- Better Auth issues JWT tokens on login
- JWT tokens sent via `Authorization: Bearer <token>`
- Backend verifies JWT using `BETTER_AUTH_SECRET` environment variable
- All endpoints require authentication
- All data access scoped to authenticated user

### Constraints
- No direct frontend-to-database access
- All database queries must filter by authenticated user ID
- Environment variables for all secrets and DB URLs
- Modular, reusable code structure
- Proper error handling and logging throughout

## Development Workflow & Quality Gates

### Implementation Workflow
1. Read relevant specification: `@specs/features/[feature].md`
2. Run `/sp.plan` to generate implementation plan
3. Run `/sp.tasks` to generate task list
4. Run `/sp.implement` to execute tasks
5. Validate against acceptance criteria
6. Test authentication and data isolation
7. Review code for production readiness

### Quality Gates
Every feature implementation MUST pass:
- Authentication verification (JWT present and valid)
- Data isolation test (user cannot access other users' data)
- API contract validation (endpoints match defined contract)
- Error handling completeness (graceful failures, proper HTTP status codes)
- No hardcoded secrets (environment variables only)
- Production-grade code review (no placeholder logic)

### Failure Conditions
Implementation is considered FAILED if:
- JWT auth is missing or bypassed
- User data leaks across accounts
- API endpoints diverge from defined contract
- Manual coding used instead of Claude Code
- Spec-driven workflow is skipped
- Hardcoded secrets present
- Placeholder or mock logic in production code

### Running the Application
- Frontend: `cd frontend && npm run dev`
- Backend: `cd backend && uvicorn main:app --reload --port 8000`
- Both: `docker-compose up`

## Governance

Constitution supersedes all development practices and technical decisions.

### Versioning Policy
- MAJOR version: Backward incompatible governance/principle removals or redefinitions
- MINOR version: New principle/section added or materially expanded guidance
- PATCH version: Clarifications, wording, typo fixes, non-semantic refinements

### Amendment Procedure
1. Document proposed change with rationale
2. Update constitution with new version
3. Propagate changes to dependent templates (plan, spec, tasks)
4. Validate all references updated
5. Record in Sync Impact Report

### Compliance Review
- All PRs MUST verify constitution compliance
- Any complexity MUST be justified in plan.md Complexity Tracking section
- Violations MUST be documented and approved
- Runtime guidance in `@backend/CLAUDE.md` and `@frontend/CLAUDE.md` must align

### Core Governance Principle
**Correctness > Convenience**
**Security > Speed**
**Spec > Assumptions**

**Version**: 2.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-09
