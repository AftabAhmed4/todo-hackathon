# Research: Landing Page + Authentication

**Feature**: 002-landing-auth
**Date**: 2026-01-09
**Purpose**: Document technical decisions and research findings for authentication implementation

## Overview

This document captures research findings and technical decisions for implementing the authentication layer of the Todo Web Application. All decisions align with the project constitution's requirements for JWT authentication, password security, and production-quality code.

---

## 1. JWT Token Management

### Decision

**Selected Approach**: JWT tokens with 24-hour expiration, stored in httpOnly cookies on the frontend, with automatic inclusion in API requests via custom fetch wrapper.

**Token Structure**:
```json
{
  "user_id": 123,
  "email": "user@example.com",
  "exp": 1704844800,
  "iat": 1704758400
}
```

**Token Signing**: HS256 algorithm with BETTER_AUTH_SECRET environment variable as the signing key.

### Rationale

1. **httpOnly Cookies**: More secure than localStorage as they're not accessible via JavaScript, preventing XSS attacks from stealing tokens
2. **24-Hour Expiration**: Balances security (limits token lifetime) with user convenience (users don't need to re-authenticate frequently during active use)
3. **HS256 Algorithm**: Symmetric signing is sufficient for this use case, simpler than asymmetric (RS256), and well-supported by python-jose and frontend libraries
4. **Minimal Claims**: Only include essential data (user_id, email) to keep token size small and avoid exposing sensitive information

### Alternatives Considered

| Alternative | Pros | Cons | Why Not Selected |
|-------------|------|------|------------------|
| localStorage | Simple to implement, works across subdomains | Vulnerable to XSS attacks, accessible via JavaScript | Security risk outweighs convenience |
| Session Storage | Cleared on tab close, slightly more secure than localStorage | Lost on tab close, still vulnerable to XSS | Poor user experience, still has XSS risk |
| Refresh Tokens | Longer session duration without security compromise | Adds complexity, requires additional endpoints | Out of scope for Phase II, can be added later |
| RS256 (Asymmetric) | Public key can be shared, more secure for distributed systems | More complex setup, requires key pair management | Overkill for single-backend architecture |

### Implementation Notes

- Frontend will use `credentials: 'include'` in fetch requests to send cookies
- Backend will set httpOnly, secure (in production), and sameSite flags on cookies
- Token expiration will be validated on every protected request
- Expired tokens will return 401 Unauthorized, triggering redirect to signin

---

## 2. Password Security

### Decision

**Selected Approach**: Bcrypt password hashing via Python's `passlib` library with automatic salt generation.

**Configuration**:
- Algorithm: bcrypt
- Rounds: 12 (default for passlib)
- Salt: Automatically generated per password
- Storage: Hash stored in `password_hash` column (VARCHAR 255)

**Password Requirements**:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- No maximum length (within reasonable limits, e.g., 128 chars)

### Rationale

1. **Bcrypt**: Industry-standard, designed specifically for password hashing, includes built-in salt, resistant to rainbow table attacks
2. **12 Rounds**: Provides strong security while maintaining acceptable performance (~100-200ms per hash)
3. **Automatic Salt**: Passlib handles salt generation automatically, reducing implementation errors
4. **Password Requirements**: Balance security with usability - strong enough to resist brute force, not so complex that users can't remember

### Alternatives Considered

| Alternative | Pros | Cons | Why Not Selected |
|-------------|------|------|------------------|
| Argon2 | Winner of Password Hashing Competition, more resistant to GPU attacks | Less widely adopted, slightly more complex setup | Bcrypt is sufficient for this use case, more mature ecosystem |
| Scrypt | Memory-hard, resistant to hardware attacks | More resource-intensive, can impact server performance | Performance concerns for high-concurrency scenarios |
| PBKDF2 | NIST-approved, widely supported | Slower than bcrypt for same security level, more vulnerable to GPU attacks | Bcrypt provides better security-performance balance |
| Plain SHA256 | Fast, simple | NOT SECURE - no salt, vulnerable to rainbow tables | Completely inadequate for password storage |

### Implementation Notes

- Use `passlib.context.CryptContext` with bcrypt scheme
- Hash passwords on signup before storing in database
- Verify passwords on signin using `verify()` method
- Never log or expose password hashes
- Validate password requirements on frontend and backend

---

## 3. Next.js 16 App Router Authentication Patterns

### Decision

**Selected Approach**: Client-side authentication state management with React Context API, server components for static content, client components for interactive auth forms.

**Architecture**:
- `AuthContext` provider wrapping the application in `layout.tsx`
- `useAuth()` hook for accessing auth state in components
- Client components for signup/signin forms (need interactivity)
- Server components for landing page (static content)
- Middleware for route protection (redirect unauthenticated users)

### Rationale

1. **Context API**: Built into React, no additional dependencies, sufficient for simple auth state (logged in/out, user info)
2. **Server Components**: Landing page can be server-rendered for better SEO and performance
3. **Client Components**: Auth forms need interactivity (form submission, validation), must be client components
4. **Middleware**: Next.js middleware runs on edge, can redirect before page loads, better UX than client-side redirects

### Alternatives Considered

| Alternative | Pros | Cons | Why Not Selected |
|-------------|------|------|------------------|
| NextAuth.js | Full-featured auth library, handles many edge cases | Heavy dependency, opinionated structure, overkill for simple JWT auth | Too complex for our needs, we're implementing custom JWT |
| Zustand | Lightweight state management, good TypeScript support | Additional dependency, learning curve | Context API is sufficient for simple auth state |
| Redux | Powerful state management, dev tools | Heavy, complex setup, overkill for auth state | Too much overhead for simple use case |
| Server-only Auth | Simpler, no client state | Poor UX (full page reloads), harder to show loading states | User experience suffers |

### Implementation Notes

- Create `AuthProvider` component wrapping app in `layout.tsx`
- Store auth state: `{ isAuthenticated: boolean, user: User | null, token: string | null }`
- Implement `login()` and `logout()` functions in context
- Use `'use client'` directive for interactive components
- Middleware checks for auth cookie, redirects to `/signin` if missing for protected routes

---

## 4. FastAPI Authentication Middleware

### Decision

**Selected Approach**: FastAPI dependency injection with `Depends()` for JWT verification on protected routes.

**Architecture**:
```python
# auth.py
def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    # Verify JWT token
    # Extract user_id from payload
    # Return user_id or raise HTTPException(401)

# Protected route example (future)
@router.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: int,
    current_user_id: int = Depends(get_current_user)
):
    if user_id != current_user_id:
        raise HTTPException(403)
    # ... fetch tasks
```

**CORS Configuration**:
- Allow origin: Frontend URL (http://localhost:3000 in dev)
- Allow credentials: True (for cookies)
- Allow methods: GET, POST, PUT, DELETE, PATCH
- Allow headers: Content-Type, Authorization

### Rationale

1. **Dependency Injection**: FastAPI's native pattern, clean separation of concerns, reusable across routes
2. **OAuth2PasswordBearer**: Standard FastAPI pattern for token extraction from Authorization header or cookies
3. **Explicit Verification**: Each protected route explicitly declares dependency on `get_current_user`, making auth requirements clear
4. **CORS with Credentials**: Required for httpOnly cookies to work across frontend-backend boundary

### Alternatives Considered

| Alternative | Pros | Cons | Why Not Selected |
|-------------|------|------|------------------|
| Global Middleware | Applies to all routes automatically | Harder to exclude public routes (signup, signin), less explicit | Auth endpoints need to be public, global middleware complicates this |
| Decorator Pattern | Pythonic, familiar to Flask users | Not FastAPI's native pattern, less integration with OpenAPI docs | Dependency injection is more idiomatic for FastAPI |
| Manual Token Parsing | Full control, no dependencies | Repetitive code, error-prone, harder to test | Dependency injection is cleaner and more maintainable |

### Implementation Notes

- Create `get_current_user()` dependency in `auth.py`
- Use `python-jose` for JWT decoding and verification
- Raise `HTTPException(401)` for invalid/expired tokens
- Raise `HTTPException(403)` for valid token but insufficient permissions
- Configure CORS in `main.py` with `CORSMiddleware`
- Public routes (signup, signin) don't use `Depends(get_current_user)`

---

## 5. Database Schema Design

### Decision

**Selected Approach**: Single `users` table with SQLModel ORM, email uniqueness constraint, and indexed email column for fast lookups.

**Schema**:
```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Indexes**:
- Primary key on `id` (automatic)
- Unique index on `email` (for fast lookup and duplicate prevention)

**Constraints**:
- `email` NOT NULL, UNIQUE
- `password_hash` NOT NULL
- `created_at` NOT NULL
- `updated_at` NOT NULL

### Rationale

1. **SQLModel**: Combines Pydantic validation with SQLAlchemy ORM, type-safe, integrates well with FastAPI
2. **Email as Unique Identifier**: Users log in with email, must be unique, indexed for fast authentication queries
3. **Separate password_hash Column**: Never store plaintext passwords, hash is stored separately
4. **Timestamps**: Track account creation and updates for auditing and debugging
5. **Integer Primary Key**: Simple, efficient, auto-incrementing, sufficient for user identification

### Alternatives Considered

| Alternative | Pros | Cons | Why Not Selected |
|-------------|------|------|------------------|
| UUID Primary Key | Globally unique, no collision risk, better for distributed systems | Larger storage, slower joins, harder to debug | Integer is sufficient for single-database setup |
| Username + Email | More flexible login options | More complex validation, username availability checking | Email-only is simpler, sufficient for MVP |
| Separate Profile Table | Cleaner separation of auth vs profile data | More joins, more complex queries | Premature optimization, no profile data yet |
| Email Verification Flag | Enables email verification feature | Out of scope for Phase II | Can be added later if needed |

### Implementation Notes

- Use SQLModel's `Field()` for column definitions
- Set `unique=True` and `index=True` on email field
- Use `datetime.utcnow` for timestamp defaults (UTC for consistency)
- Create database tables with `SQLModel.metadata.create_all(engine)`
- Handle unique constraint violations (duplicate email) with try-except, return 400 Bad Request

---

## Technology Stack Summary

### Backend
- **Framework**: FastAPI 0.104+
- **ORM**: SQLModel 0.0.14+
- **Database**: Neon Serverless PostgreSQL
- **JWT**: python-jose[cryptography] 3.3+
- **Password Hashing**: passlib[bcrypt] 1.7+
- **CORS**: fastapi.middleware.cors (built-in)

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS 3+
- **HTTP Client**: Native fetch API with custom wrapper
- **State Management**: React Context API (built-in)

### Development Tools
- **Backend Testing**: pytest, httpx (if tests requested)
- **Frontend Testing**: Jest, React Testing Library (if tests requested)
- **Database Migrations**: Alembic (if needed for schema changes)

---

## Security Considerations

### Implemented Security Measures

1. **Password Security**:
   - Bcrypt hashing with automatic salt
   - Minimum password requirements enforced
   - No plaintext password storage or logging

2. **Token Security**:
   - JWT tokens with expiration
   - httpOnly cookies prevent XSS token theft
   - Secure flag in production (HTTPS only)
   - sameSite flag prevents CSRF attacks

3. **API Security**:
   - CORS configured to allow only frontend origin
   - Input validation on all endpoints (Pydantic models)
   - Error messages don't reveal whether emails exist (generic "invalid credentials")
   - Rate limiting recommended for production (out of scope for Phase II)

4. **Database Security**:
   - Unique constraint prevents duplicate accounts
   - SQLModel ORM prevents SQL injection
   - Database credentials in environment variables only

### Known Limitations (Out of Scope)

- No rate limiting (vulnerable to brute force attacks)
- No CAPTCHA (vulnerable to automated attacks)
- No email verification (accounts active immediately)
- No password reset (users can't recover forgotten passwords)
- No account lockout (no protection against repeated failed logins)
- No audit logging (no record of authentication attempts)

These limitations are acceptable for Phase II (hackathon demo) but should be addressed before production deployment.

---

## Performance Considerations

### Expected Performance

- **Password Hashing**: ~100-200ms per operation (bcrypt with 12 rounds)
- **JWT Verification**: <10ms per operation (symmetric key verification)
- **Database Queries**: <50ms for user lookup by email (indexed)
- **Total Signup Time**: ~200-300ms (hash + insert)
- **Total Signin Time**: ~150-250ms (lookup + verify + token generation)

### Optimization Opportunities

1. **Caching**: User data could be cached after authentication (not implemented in Phase II)
2. **Connection Pooling**: SQLModel/SQLAlchemy handles this automatically
3. **Async Operations**: FastAPI runs async by default, no additional optimization needed
4. **CDN**: Frontend static assets could be served via CDN (deployment concern, not implementation)

---

## Conclusion

All technical decisions documented in this research align with the project constitution's requirements:
- ✅ JWT-based stateless authentication
- ✅ Secure password storage (bcrypt hashing)
- ✅ User data isolation (unique user_id for future data scoping)
- ✅ Production-quality patterns (no mock auth, comprehensive error handling)
- ✅ No hardcoded secrets (environment variables for all sensitive data)

The selected technologies and patterns are industry-standard, well-documented, and appropriate for a hackathon-scale application with production-quality code.

**Next Phase**: Proceed to Phase 1 (Design & Contracts) to generate data models and API specifications.
