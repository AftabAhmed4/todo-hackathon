# Data Model: Landing Page + Authentication

**Feature**: 002-landing-auth
**Date**: 2026-01-09
**Purpose**: Define data entities, relationships, and validation rules for authentication

## Overview

This document defines the data model for the authentication feature. The primary entity is the User, which represents an individual account in the system. This model establishes the foundation for user data isolation in future features (tasks, etc.).

---

## Entity: User

### Description

Represents an individual user account in the Todo Web Application. Each user has a unique identifier, email address, and securely hashed password. Users authenticate using their email and password to receive JWT tokens for accessing protected resources.

### Fields

| Field Name | Type | Constraints | Description |
|------------|------|-------------|-------------|
| `id` | Integer | PRIMARY KEY, AUTO_INCREMENT, NOT NULL | Unique identifier for the user. Auto-generated on account creation. |
| `email` | String (255) | UNIQUE, NOT NULL, INDEX | User's email address. Used for login and must be unique across all users. |
| `password_hash` | String (255) | NOT NULL | Bcrypt hash of the user's password. Never store plaintext passwords. |
| `created_at` | DateTime | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Timestamp when the account was created (UTC). |
| `updated_at` | DateTime | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Timestamp when the account was last updated (UTC). |

### Indexes

- **Primary Index**: `id` (automatic with PRIMARY KEY)
- **Unique Index**: `email` (for fast lookup during authentication and duplicate prevention)

### Validation Rules

#### Email Validation
- **Format**: Must match standard email pattern (contains @, valid domain structure)
- **Length**: Maximum 255 characters
- **Uniqueness**: Must not already exist in the database
- **Case Sensitivity**: Stored as-is, but lookups should be case-insensitive (convert to lowercase before query)
- **Trimming**: Leading/trailing whitespace should be removed before storage

**Validation Logic**:
```python
# Frontend validation (TypeScript)
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!emailRegex.test(email)) {
    throw new Error("Invalid email format");
}

# Backend validation (Python/Pydantic)
from pydantic import EmailStr, Field

class SignupRequest(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
```

#### Password Validation
- **Minimum Length**: 8 characters
- **Maximum Length**: 128 characters (reasonable limit to prevent DoS)
- **Complexity Requirements**:
  - At least one uppercase letter (A-Z)
  - At least one lowercase letter (a-z)
  - At least one number (0-9)
- **Forbidden Characters**: None (allow special characters for stronger passwords)
- **Hashing**: Must be hashed with bcrypt before storage (never store plaintext)

**Validation Logic**:
```python
# Frontend validation (TypeScript)
function validatePassword(password: string): boolean {
    if (password.length < 8) return false;
    if (!/[A-Z]/.test(password)) return false;
    if (!/[a-z]/.test(password)) return false;
    if (!/[0-9]/.test(password)) return false;
    return true;
}

# Backend validation (Python)
import re

def validate_password(password: str) -> bool:
    if len(password) < 8 or len(password) > 128:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True
```

### Relationships

#### Current Relationships
- None (User is the root entity for this feature)

#### Future Relationships
- **User → Tasks** (One-to-Many): Each user will own multiple tasks
  - Foreign key: `tasks.user_id → users.id`
  - Cascade: DELETE CASCADE (when user is deleted, all their tasks are deleted)
  - This relationship will be implemented in the next feature (Task CRUD)

### State Transitions

Users have a simple lifecycle with no explicit state field:

1. **Created**: User account is created via signup endpoint
   - Initial state: Account exists with hashed password
   - Transition: User can immediately sign in

2. **Active**: User can authenticate and access the application
   - State: Normal operation
   - Transition: User signs in, receives JWT token

3. **Authenticated Session**: User has valid JWT token
   - State: Token is valid and not expired
   - Transition: Token expires after 24 hours, user must sign in again

**Note**: Account deletion, suspension, and email verification are out of scope for Phase II.

### SQLModel Implementation

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    """
    User account entity for authentication.

    Represents an individual user with email/password credentials.
    Each user has a unique ID used for data isolation in future features.
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User's email address (unique, used for login)"
    )
    password_hash: str = Field(
        max_length=255,
        description="Bcrypt hash of user's password (never store plaintext)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC)"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "password_hash": "$2b$12$...",
                "created_at": "2026-01-09T12:00:00Z",
                "updated_at": "2026-01-09T12:00:00Z"
            }
        }
```

---

## Entity: JWT Token (Logical Entity)

### Description

JWT tokens are not stored in the database but are logical entities representing authenticated sessions. Tokens are issued on successful signup/signin and verified on protected requests.

### Token Payload Structure

```json
{
  "user_id": 123,
  "email": "user@example.com",
  "exp": 1704844800,
  "iat": 1704758400
}
```

### Fields

| Field Name | Type | Description |
|------------|------|-------------|
| `user_id` | Integer | User's unique identifier (from users.id) |
| `email` | String | User's email address (for convenience, not used for authorization) |
| `exp` | Integer | Expiration timestamp (Unix epoch, 24 hours from issuance) |
| `iat` | Integer | Issued-at timestamp (Unix epoch, time of token creation) |

### Validation Rules

- **Signature**: Must be valid (signed with BETTER_AUTH_SECRET)
- **Expiration**: Must not be expired (exp > current time)
- **User ID**: Must be a positive integer
- **Email**: Must be a valid email format (informational only)

### Token Lifecycle

1. **Issuance**: Token created on successful signup or signin
2. **Storage**: Token stored in httpOnly cookie on frontend
3. **Usage**: Token sent with every API request in Authorization header or cookie
4. **Verification**: Backend verifies signature and expiration on protected requests
5. **Expiration**: Token becomes invalid after 24 hours, user must sign in again

---

## Database Schema (SQL)

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index on email for fast authentication lookups
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Trigger to update updated_at timestamp (PostgreSQL)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Note**: SQLModel will handle table creation automatically. The SQL above is for reference and manual database setup if needed.

---

## Data Flow Diagrams

### Signup Flow

```
User Input (email, password)
    ↓
Frontend Validation (format, requirements)
    ↓
POST /api/auth/signup
    ↓
Backend Validation (Pydantic)
    ↓
Check Email Uniqueness (SELECT email FROM users WHERE email = ?)
    ↓
Hash Password (bcrypt)
    ↓
Insert User (INSERT INTO users ...)
    ↓
Generate JWT Token (user_id, email, exp)
    ↓
Return Token + User Info
    ↓
Frontend Stores Token (httpOnly cookie)
    ↓
Redirect to /tasks
```

### Signin Flow

```
User Input (email, password)
    ↓
Frontend Validation (format)
    ↓
POST /api/auth/signin
    ↓
Backend Validation (Pydantic)
    ↓
Lookup User (SELECT * FROM users WHERE email = ?)
    ↓
Verify Password (bcrypt.verify)
    ↓
Generate JWT Token (user_id, email, exp)
    ↓
Return Token + User Info
    ↓
Frontend Stores Token (httpOnly cookie)
    ↓
Redirect to /tasks
```

### Token Verification Flow (Future Protected Requests)

```
API Request with Token
    ↓
Extract Token (from Authorization header or cookie)
    ↓
Verify Signature (JWT.verify with BETTER_AUTH_SECRET)
    ↓
Check Expiration (exp > current_time)
    ↓
Extract user_id from Payload
    ↓
Proceed with Request (user_id available for data scoping)
```

---

## Error Handling

### Database Errors

| Error | HTTP Status | User Message | Technical Details |
|-------|-------------|--------------|-------------------|
| Duplicate Email | 400 Bad Request | "Email already registered" | UNIQUE constraint violation on email |
| Invalid Email Format | 400 Bad Request | "Invalid email format" | Pydantic validation failure |
| Password Too Weak | 400 Bad Request | "Password must be at least 8 characters with uppercase, lowercase, and number" | Custom validation failure |
| Database Connection Error | 500 Internal Server Error | "Service temporarily unavailable" | Database connection failed |
| User Not Found | 401 Unauthorized | "Invalid email or password" | Email doesn't exist (generic message for security) |
| Invalid Password | 401 Unauthorized | "Invalid email or password" | Password verification failed (generic message for security) |

### Security Considerations

- **Generic Error Messages**: Signin errors don't reveal whether email exists (prevents user enumeration)
- **No Password Hints**: Never return information about password requirements in error messages after failed signin
- **Rate Limiting**: Not implemented in Phase II, but recommended for production to prevent brute force attacks

---

## Migration Strategy

### Initial Schema Creation

SQLModel will create tables automatically on first run:

```python
from sqlmodel import SQLModel, create_engine

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)
```

### Future Migrations

When adding the tasks table (next feature):

```python
# New Task model will reference User
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    # ... other fields
```

SQLModel will handle foreign key creation automatically.

---

## Testing Considerations

### Data Validation Tests

1. **Email Validation**:
   - Valid email formats accepted
   - Invalid formats rejected
   - Duplicate emails rejected
   - Case-insensitive email matching

2. **Password Validation**:
   - Minimum length enforced
   - Complexity requirements enforced
   - Hashing applied before storage
   - Verification works correctly

3. **Timestamp Management**:
   - created_at set on insert
   - updated_at updated on modification

### Database Integrity Tests

1. **Unique Constraints**: Duplicate email insertion fails
2. **Foreign Keys**: (Future) Tasks reference valid users
3. **Indexes**: Email lookups are fast (<50ms)

---

## Conclusion

This data model establishes the foundation for user authentication and data isolation. The User entity is simple but production-ready, with proper validation, indexing, and security measures. Future features (tasks, etc.) will build on this foundation by adding foreign key relationships to the users table.

**Next Steps**: Generate API contracts defining the authentication endpoints that interact with this data model.
