# Implementation Plan: Landing Page + Authentication

**Branch**: `002-landing-auth` | **Date**: 2026-01-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-landing-auth/spec.md`

**Note**: This plan implements the authentication foundation for the multi-user todo application, including landing page, user registration, and login functionality with JWT-based authentication.

## Summary

This feature implements the authentication layer for the Todo Web Application, enabling multi-user access with secure JWT-based authentication. The implementation includes:

1. **Landing Page**: Public-facing page describing the application with clear calls-to-action for signup and signin
2. **User Registration**: New users can create accounts with email/password credentials, with validation and secure password storage
3. **User Login**: Existing users can authenticate and receive JWT tokens for accessing protected resources
4. **JWT Authentication**: Stateless token-based authentication with secure token storage and automatic inclusion in API requests
5. **User Data Isolation**: Each user account is associated with a unique user ID, enabling strict data isolation for future todo features

The technical approach follows the project constitution's requirements for JWT authentication, password hashing, user data isolation, and production-quality code.

## Technical Context

**Language/Version**:
- Frontend: TypeScript with Next.js 16+ (App Router)
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: Next.js 16+, React 18+, Tailwind CSS, TypeScript
- Backend: FastAPI, SQLModel, Pydantic, python-jose (JWT), passlib (password hashing), python-multipart

**Storage**: Neon Serverless PostgreSQL (users table with email, password_hash, timestamps)

**Testing**:
- Frontend: Jest + React Testing Library (if tests requested)
- Backend: pytest + httpx (if tests requested)

**Target Platform**:
- Frontend: Web browsers (desktop and mobile, 320px minimum width)
- Backend: Linux server (containerized deployment)

**Project Type**: Web application (monorepo with frontend/ and backend/ folders)

**Performance Goals**:
- Landing page load: <3 seconds on standard broadband
- Authentication response: <2 seconds for signup/signin
- Token validation: <100ms per request

**Constraints**:
- No email verification (out of scope for this phase)
- No password reset (out of scope for this phase)
- No rate limiting (should be added in production)
- JWT tokens expire after 24 hours (configurable)
- Passwords must meet minimum security requirements (8+ chars, uppercase, lowercase, number)

**Scale/Scope**:
- Expected users: 100-1000 concurrent users (hackathon demo scale)
- Database: Single Neon PostgreSQL instance
- Authentication endpoints: 2 (signup, signin)
- Frontend pages: 3 (landing, signup, signin)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Required Gate Verification

- [x] **Spec-Driven Workflow**: Feature implementation will follow Spec-Kit Plus → Claude Code → Tasks → Implementation workflow. No manual coding.
  - ✅ Specification created at specs/002-landing-auth/spec.md
  - ✅ This plan follows spec requirements exactly
  - ✅ Tasks will be generated from this plan via /sp.tasks
  - ✅ Implementation will be executed via /sp.implement

- [x] **Database Isolation**: All database operations use SQLModel with user-scoped queries via foreign key. No direct frontend-to-database access.
  - ✅ Users table will use SQLModel ORM
  - ✅ Each user has unique user_id for future data scoping
  - ✅ Frontend communicates only via backend API (no direct DB access)
  - ✅ Future tasks table will have foreign key to users.id

- [x] **JWT Authentication**: All API endpoints secured with JWT tokens. Better Auth issues tokens, backend verifies using BETTER_AUTH_SECRET.
  - ✅ Backend will issue JWT tokens on successful signup/signin
  - ✅ JWT tokens will include user_id claim
  - ✅ Backend will verify JWT signature using BETTER_AUTH_SECRET environment variable
  - ✅ Frontend will store and attach tokens to all API requests
  - ⚠️ NOTE: This feature implements authentication endpoints (/signup, /signin) which are PUBLIC by design. Future protected endpoints (tasks CRUD) will require JWT verification.

- [x] **API Contract**: Endpoints match defined contract (/api/{user_id}/tasks/*). No divergence from specified paths.
  - ✅ Authentication endpoints: POST /api/auth/signup, POST /api/auth/signin (public endpoints)
  - ✅ Future task endpoints will follow /api/{user_id}/tasks/* pattern
  - ✅ No custom or non-standard endpoint patterns

- [x] **Frontend Auth State**: Frontend handles auth state, API client automatically attaches JWT tokens. UI reflects only authenticated user data.
  - ✅ Frontend will manage authentication state (logged in/out)
  - ✅ API client will automatically include Authorization header with JWT
  - ✅ Authenticated users will be redirected to /tasks (future feature)
  - ✅ Unauthenticated users will be redirected to /signin for protected pages

- [x] **Monorepo Structure**: Implementation fits in frontend/ and backend/ folders. Spec-Kit files at root or /specs.
  - ✅ Frontend code in frontend/app/ (Next.js App Router)
  - ✅ Backend code in backend/ (FastAPI)
  - ✅ Spec files in specs/002-landing-auth/
  - ✅ Shared environment variables documented

- [x] **No Hardcoded Secrets**: All secrets and DB URLs via environment variables. No hardcoded values in code.
  - ✅ DATABASE_URL from environment
  - ✅ BETTER_AUTH_SECRET from environment (JWT signing key)
  - ✅ All secrets documented in .env.example
  - ✅ No hardcoded passwords, tokens, or connection strings

- [x] **Production Quality**: Code is reviewable, production-grade. No placeholder logic, mock auth, or insecure shortcuts.
  - ✅ Real password hashing with bcrypt/passlib
  - ✅ Real JWT token generation and verification
  - ✅ Comprehensive error handling with appropriate HTTP status codes
  - ✅ Input validation on all endpoints
  - ✅ No mock authentication or placeholder logic

### Complexity Tracking Justification

No violations. All constitution requirements are met by this implementation plan.

## Project Structure

### Documentation (this feature)

```text
specs/002-landing-auth/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/           # Phase 1 output (to be generated)
│   ├── auth-api.yaml    # OpenAPI spec for auth endpoints
│   └── user-model.yaml  # User entity schema
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI app entry point
├── models.py            # SQLModel User model
├── auth.py              # JWT utilities (create_token, verify_token)
├── routes/
│   └── auth.py          # Auth endpoints (signup, signin)
├── db.py                # Database connection and session management
├── schemas.py           # Pydantic request/response models
└── requirements.txt     # Python dependencies

frontend/
├── app/
│   ├── layout.tsx       # Root layout with auth provider
│   ├── page.tsx         # Landing page (/)
│   ├── signup/
│   │   └── page.tsx     # Signup page (/signup)
│   ├── signin/
│   │   └── page.tsx     # Signin page (/signin)
│   └── tasks/
│       └── page.tsx     # Protected tasks page (future feature)
├── components/
│   ├── Header.tsx       # Navigation header
│   ├── Footer.tsx       # Page footer
│   ├── AuthForm.tsx     # Reusable auth form component
│   └── AuthGuard.tsx    # Protected route wrapper
├── lib/
│   ├── api.ts           # API client with JWT handling
│   ├── auth.ts          # Auth context and hooks
│   └── types.ts         # TypeScript type definitions
├── tailwind.config.js   # Tailwind CSS configuration
└── package.json         # Node dependencies
```

**Structure Decision**: Web application structure (Option 2) selected. This is a full-stack web application with separate frontend (Next.js) and backend (FastAPI) folders. The monorepo structure enables Claude Code to reason about both sides together while maintaining clear separation of concerns.

## Complexity Tracking

No complexity violations. This implementation follows standard patterns:
- Standard JWT authentication (no custom auth schemes)
- Standard REST API endpoints (no complex protocols)
- Standard password hashing (bcrypt via passlib)
- Standard database schema (users table with standard fields)
- Standard frontend routing (Next.js App Router)

---

## Phase 0: Research & Technical Decisions

### Research Topics

Based on the Technical Context, the following research areas have been identified:

1. **JWT Token Management**
   - Best practices for JWT token expiration and refresh
   - Secure token storage on frontend (httpOnly cookies vs localStorage)
   - Token payload structure and claims

2. **Password Security**
   - Password hashing algorithm selection (bcrypt, argon2, scrypt)
   - Salt generation and storage
   - Password validation rules

3. **Next.js 16 App Router Authentication Patterns**
   - Server components vs client components for auth
   - Middleware for route protection
   - Auth context and state management

4. **FastAPI Authentication Middleware**
   - Dependency injection for JWT verification
   - Error handling for authentication failures
   - CORS configuration for frontend-backend communication

5. **Database Schema Design**
   - User table structure and indexes
   - Email uniqueness constraints
   - Timestamp management (created_at, updated_at)

### Research Output

Research findings will be documented in `research.md` with decisions, rationale, and alternatives considered for each topic.

---

## Phase 1: Design & Contracts

### Data Model Design

The data model will be documented in `data-model.md` with:
- User entity structure
- Field types and constraints
- Relationships (for future features)
- Validation rules

### API Contracts

API contracts will be generated in `/contracts/` directory:
- `auth-api.yaml`: OpenAPI specification for authentication endpoints
- `user-model.yaml`: User entity schema

### Quickstart Guide

The `quickstart.md` will provide:
- Environment setup instructions
- Database initialization steps
- Running frontend and backend
- Testing authentication flows

---

## Next Steps

After this plan is complete:
1. Review and approve this implementation plan
2. Run `/sp.tasks` to generate task breakdown
3. Run `/sp.implement` to execute tasks via Claude Code
4. Test authentication flows (signup, signin, JWT verification)
5. Validate constitution compliance (JWT auth, user isolation, production quality)
