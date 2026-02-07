# Quickstart Guide: Landing Page + Authentication

**Feature**: 002-landing-auth
**Date**: 2026-01-09
**Purpose**: Step-by-step guide to set up, run, and test the authentication feature

## Overview

This guide walks you through setting up the development environment, running the frontend and backend, and testing the authentication flows (signup, signin, JWT verification). Follow these steps in order for a smooth setup experience.

---

## Prerequisites

### Required Software

- **Node.js**: Version 18+ (for Next.js frontend)
- **Python**: Version 3.11+ (for FastAPI backend)
- **PostgreSQL**: Neon Serverless PostgreSQL account (or local PostgreSQL 14+)
- **Git**: For version control
- **Code Editor**: VS Code, Cursor, or similar

### Verify Installations

```bash
# Check Node.js version
node --version  # Should be v18.0.0 or higher

# Check Python version
python --version  # Should be 3.11.0 or higher

# Check npm version
npm --version  # Should be 8.0.0 or higher

# Check pip version
pip --version  # Should be 23.0.0 or higher
```

---

## Step 1: Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd hackathon-todo

# Checkout the feature branch
git checkout 002-landing-auth
```

---

## Step 2: Environment Setup

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cd backend
touch .env
```

Add the following environment variables:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/database_name

# JWT Secret (generate a secure random string)
BETTER_AUTH_SECRET=your-super-secret-jwt-signing-key-change-this-in-production

# Server Configuration
API_PORT=8000
ENVIRONMENT=development

# CORS Configuration (frontend URL)
FRONTEND_URL=http://localhost:3000
```

**Generate a secure JWT secret**:
```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Using OpenSSL
openssl rand -base64 32
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
cd ../frontend
touch .env.local
```

Add the following environment variables:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
```

### Database Setup (Neon PostgreSQL)

1. **Create Neon Account**: Visit [neon.tech](https://neon.tech) and sign up
2. **Create New Project**: Click "New Project" in the dashboard
3. **Get Connection String**: Copy the connection string from project settings
4. **Update DATABASE_URL**: Paste the connection string in `backend/.env`

**Connection String Format**:
```
postgresql://username:password@hostname/database?sslmode=require
```

---

## Step 3: Install Dependencies

### Backend Dependencies

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlmodel pydantic python-jose[cryptography] passlib[bcrypt] python-multipart psycopg2-binary

# Or install from requirements.txt (if available)
pip install -r requirements.txt
```

### Frontend Dependencies

```bash
cd ../frontend

# Install dependencies
npm install

# Or use yarn
yarn install
```

---

## Step 4: Initialize Database

### Create Database Tables

The backend will automatically create tables on first run, but you can manually initialize:

```bash
cd backend

# Run Python script to create tables
python -c "
from sqlmodel import SQLModel, create_engine
from models import User
import os

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)
print('Database tables created successfully')
"
```

### Verify Database Connection

```bash
# Test database connection
python -c "
from sqlmodel import create_engine
import os

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
connection = engine.connect()
print('Database connection successful')
connection.close()
"
```

---

## Step 5: Run the Application

### Start Backend Server

```bash
cd backend

# Activate virtual environment (if not already activated)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run FastAPI server with auto-reload
uvicorn main:app --reload --port 8000

# Server should start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Start Frontend Server

Open a new terminal window:

```bash
cd frontend

# Run Next.js development server
npm run dev

# Or with yarn
yarn dev

# Server should start at http://localhost:3000
```

**Expected Output**:
```
   ▲ Next.js 16.0.0
   - Local:        http://localhost:3000
   - Network:      http://192.168.1.100:3000

 ✓ Ready in 2.5s
```

---

## Step 6: Test Authentication Flows

### Test 1: Landing Page

1. **Open Browser**: Navigate to `http://localhost:3000`
2. **Verify Content**: Landing page should display:
   - Application description
   - "Sign Up" button (prominent)
   - "Sign In" link
   - Responsive layout on mobile

**Expected Result**: Landing page loads in <3 seconds with clear calls-to-action.

### Test 2: User Signup

1. **Navigate to Signup**: Click "Sign Up" button or go to `http://localhost:3000/signup`
2. **Enter Valid Credentials**:
   - Email: `test@example.com`
   - Password: `TestPass123`
3. **Submit Form**: Click "Sign Up" button
4. **Verify Success**:
   - User account created
   - JWT token received
   - Redirected to `/tasks` (or dashboard)

**Expected Result**: Account created in <2 seconds, token stored in cookie, redirect successful.

**Test Invalid Inputs**:
- **Duplicate Email**: Try signing up with same email → Error: "Email already registered"
- **Weak Password**: Try `test123` → Error: "Password must be at least 8 characters with uppercase, lowercase, and number"
- **Invalid Email**: Try `notanemail` → Error: "Invalid email format"

### Test 3: User Signin

1. **Navigate to Signin**: Go to `http://localhost:3000/signin`
2. **Enter Credentials**:
   - Email: `test@example.com`
   - Password: `TestPass123`
3. **Submit Form**: Click "Sign In" button
4. **Verify Success**:
   - Authentication successful
   - JWT token received
   - Redirected to `/tasks`

**Expected Result**: Signin completes in <2 seconds, token stored, redirect successful.

**Test Invalid Inputs**:
- **Wrong Password**: Try incorrect password → Error: "Invalid email or password"
- **Non-existent Email**: Try unregistered email → Error: "Invalid email or password" (same message for security)

### Test 4: JWT Token Verification

1. **Open Browser DevTools**: Press F12
2. **Go to Application Tab**: Check Cookies
3. **Verify Token Cookie**:
   - Name: `token`
   - Value: JWT string (starts with `eyJ...`)
   - HttpOnly: ✓ (checked)
   - Secure: ✓ (in production)
   - SameSite: Strict

**Expected Result**: Token cookie present with correct security flags.

### Test 5: API Endpoints (Manual Testing)

#### Test Signup Endpoint

```bash
# Using curl
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "api-test@example.com",
    "password": "ApiTest123"
  }'

# Expected Response (201 Created):
{
  "user": {
    "id": 2,
    "email": "api-test@example.com",
    "created_at": "2026-01-09T12:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Account created successfully"
}
```

#### Test Signin Endpoint

```bash
# Using curl
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "api-test@example.com",
    "password": "ApiTest123"
  }'

# Expected Response (200 OK):
{
  "user": {
    "id": 2,
    "email": "api-test@example.com",
    "created_at": "2026-01-09T12:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Signed in successfully"
}
```

---

## Step 7: Verify Database

### Check Users Table

```bash
# Connect to Neon PostgreSQL
psql $DATABASE_URL

# List all users
SELECT id, email, created_at FROM users;

# Expected Output:
 id |         email          |       created_at
----+------------------------+------------------------
  1 | test@example.com       | 2026-01-09 12:00:00+00
  2 | api-test@example.com   | 2026-01-09 12:05:00+00

# Exit psql
\q
```

---

## Troubleshooting

### Backend Issues

#### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution**: Install dependencies in virtual environment
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: "sqlalchemy.exc.OperationalError: could not connect to server"
**Solution**: Check DATABASE_URL in `.env` file
```bash
# Verify connection string format
echo $DATABASE_URL

# Test connection
python -c "from sqlmodel import create_engine; import os; engine = create_engine(os.getenv('DATABASE_URL')); engine.connect()"
```

#### Issue: "jose.exceptions.JWTError: Invalid token"
**Solution**: Check BETTER_AUTH_SECRET is set correctly
```bash
# Verify secret is set
echo $BETTER_AUTH_SECRET

# Generate new secret if needed
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Frontend Issues

#### Issue: "Error: Cannot find module 'next'"
**Solution**: Install dependencies
```bash
cd frontend
npm install
```

#### Issue: "Failed to fetch" when calling API
**Solution**: Check CORS configuration and backend URL
```bash
# Verify backend is running
curl http://localhost:8000/docs

# Check NEXT_PUBLIC_API_URL in .env.local
cat .env.local
```

#### Issue: "Cookie not being set"
**Solution**: Check CORS credentials configuration
- Backend: `allow_credentials=True` in CORS middleware
- Frontend: `credentials: 'include'` in fetch requests

### Database Issues

#### Issue: "relation 'users' does not exist"
**Solution**: Create database tables
```bash
cd backend
python -c "from sqlmodel import SQLModel, create_engine; from models import User; import os; engine = create_engine(os.getenv('DATABASE_URL')); SQLModel.metadata.create_all(engine)"
```

#### Issue: "duplicate key value violates unique constraint"
**Solution**: Email already exists, use different email or delete existing user
```bash
# Connect to database
psql $DATABASE_URL

# Delete user
DELETE FROM users WHERE email = 'test@example.com';
```

---

## Development Workflow

### Making Changes

1. **Backend Changes**: Edit files in `backend/`, server auto-reloads
2. **Frontend Changes**: Edit files in `frontend/`, page auto-refreshes
3. **Database Changes**: Update models in `models.py`, recreate tables

### Testing Changes

1. **Manual Testing**: Use browser and curl commands above
2. **API Documentation**: Visit `http://localhost:8000/docs` for interactive API testing
3. **Database Inspection**: Use psql or Neon dashboard to inspect data

### Debugging

1. **Backend Logs**: Check terminal running uvicorn for error messages
2. **Frontend Logs**: Check browser console (F12) for errors
3. **Network Tab**: Inspect API requests/responses in browser DevTools

---

## Next Steps

After completing this quickstart:

1. **Run `/sp.tasks`**: Generate task breakdown for implementation
2. **Run `/sp.implement`**: Execute tasks via Claude Code
3. **Test Thoroughly**: Verify all acceptance criteria from spec.md
4. **Validate Constitution**: Ensure JWT auth, user isolation, production quality

---

## Quick Reference

### Start Development Servers

```bash
# Terminal 1: Backend
cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev
```

### Environment Variables

| Variable | Location | Purpose |
|----------|----------|---------|
| `DATABASE_URL` | backend/.env | PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | backend/.env | JWT signing key |
| `NEXT_PUBLIC_API_URL` | frontend/.env.local | Backend API endpoint |

### Key URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Landing Page**: http://localhost:3000
- **Signup**: http://localhost:3000/signup
- **Signin**: http://localhost:3000/signin

### Test Credentials

```
Email: test@example.com
Password: TestPass123
```

---

## Support

If you encounter issues not covered in this guide:

1. Check the [specification](./spec.md) for requirements
2. Review the [implementation plan](./plan.md) for technical details
3. Consult the [research document](./research.md) for technical decisions
4. Check the [API contracts](./contracts/) for endpoint specifications

---

**Last Updated**: 2026-01-09
**Feature Branch**: 002-landing-auth
**Status**: Ready for implementation
