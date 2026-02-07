# Todo App - Hackathon II

A secure, multi-user todo application with **AI-powered chatbot** built with Next.js, FastAPI, and OpenAI.

## 🌟 Key Features

### 🤖 AI Todo Assistant (NEW!)
- **Natural Language Interface**: Manage todos through conversational AI
- **Smart Tool Selection**: AI automatically chooses the right action
- **Context-Aware**: Maintains conversation history for better understanding
- **5 MCP Tools**: Create, list, update, delete, and complete todos via chat

### 🔐 Secure Authentication
- **JWT-based authentication** with httpOnly cookies
- **User Registration**: Create accounts with email and password validation
- **User Login**: Authenticate existing users with secure password verification
- **Password Security**: Bcrypt hashing with 12 rounds
- **Protected Routes**: Automatic redirect for unauthenticated users

### 💻 Modern Stack
- **Frontend**: Next.js 16 (App Router) + React 18 + TypeScript + Tailwind CSS
- **Backend**: FastAPI + SQLModel + PostgreSQL (Neon)
- **AI**: OpenAI GPT-4o with function calling
- **Architecture**: Stateless MCP tools + Conversation history

## Technology Stack

### Frontend
- **Next.js 16** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Custom Chat UI** - Real-time conversational interface

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM
- **Neon PostgreSQL** - Serverless PostgreSQL database
- **OpenAI API** - GPT-4o for natural language understanding
- **MCP Tools** - Stateless function calling architecture
- **python-jose** - JWT token handling
- **passlib** - Password hashing with bcrypt

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.12+
- **PostgreSQL** database (Neon recommended)
- **OpenAI API Key** (required for AI chatbot)

## Project Structure

```
hackathon-todo/
├── backend/              # FastAPI backend
│   ├── main.py          # Application entry point
│   ├── models.py        # Database models (User, Task, Conversation, Message)
│   ├── mcp_tools.py     # MCP tool implementations (5 CRUD tools)
│   ├── agent.py         # OpenAI Agent configuration
│   ├── db.py            # Database connection
│   ├── auth.py          # JWT utilities
│   ├── schemas.py       # Pydantic schemas
│   ├── routes/          # API route handlers
│   │   ├── auth.py      # Authentication endpoints
│   │   ├── tasks.py     # Task CRUD endpoints
│   │   └── chat.py      # AI Chat endpoints (NEW!)
│   ├── requirements.txt # Python dependencies
│   ├── .env             # Environment variables (create from .env.example)
│   └── .env.example     # Environment template
│
├── frontend/            # Next.js frontend
│   ├── app/             # App Router pages
│   │   ├── layout.tsx   # Root layout
│   │   ├── page.tsx     # Landing page
│   │   ├── signup/      # Signup page
│   │   ├── signin/      # Signin page
│   │   ├── chat/        # AI Chat page (NEW!)
│   │   └── tasks/       # Tasks page (protected)
│   ├── components/      # Reusable components
│   │   ├── ChatInterface.tsx  # AI Chat UI (NEW!)
│   │   ├── Header.tsx   # Navigation header
│   │   └── Footer.tsx   # Footer component
│   ├── lib/             # Utilities
│   │   ├── api.ts       # API client (with chat methods)
│   │   ├── auth.ts      # Auth context
│   │   └── types.ts     # TypeScript types (with chat types)
│   ├── package.json     # Node dependencies
│   ├── .env.local       # Environment variables (create from .env.example)
│   └── .env.example     # Environment template
│
└── specs/               # Feature specifications
    └── 002-landing-auth/
        ├── spec.md      # Feature specification
        ├── plan.md      # Implementation plan
        └── tasks.md     # Task breakdown
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hackathon-todo
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
# Database connection string (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host/database

# JWT secret key (generate a secure random string)
BETTER_AUTH_SECRET=your-secret-key-here-min-32-chars

# OpenAI API Key (REQUIRED for AI chatbot)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000
```

**Generate a secure secret key:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Run the Backend

```bash
uvicorn main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`

### 3. Frontend Setup

#### Install Node Dependencies

```bash
cd frontend
npm install
```

#### Configure Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
cp .env.example .env.local
```

Edit `.env.local` and add your configuration:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Run the Frontend

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Environment Variables

### Backend (.env)

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | `postgresql://user:pass@host/db` |
| `BETTER_AUTH_SECRET` | JWT secret key (min 32 chars) | Yes | `your-secret-key-here` |
| `OPENAI_API_KEY` | OpenAI API key for AI chatbot | Yes | `sk-your-key-here` |
| `FRONTEND_URL` | Frontend URL for CORS | No | `http://localhost:3000` (default) |

### Frontend (.env.local)

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes | `http://localhost:8000` |

## 🚀 Quick Start

For a quick 5-minute setup guide, see **[QUICKSTART.md](QUICKSTART.md)**

For detailed implementation documentation, see **[IMPLEMENTATION.md](IMPLEMENTATION.md)**

## API Endpoints

### AI Chat (NEW!)

#### POST /api/chat/
Send a message to the AI assistant.

**Request Body:**
```json
{
  "message": "Add a todo to buy groceries",
  "conversation_id": 1  // optional, omit for new conversation
}
```

**Response:**
```json
{
  "response": "Todo 'buy groceries' created successfully",
  "conversation_id": 1,
  "message_id": 2,
  "tool_calls": [
    {
      "tool": "create_todo",
      "arguments": {"title": "buy groceries", "user_id": 1},
      "result": {"success": true, "todo": {...}}
    }
  ]
}
```

#### GET /api/chat/conversations
List all conversations for the authenticated user.

#### GET /api/chat/conversations/{id}/messages
Get all messages in a specific conversation.

### Authentication

#### POST /api/auth/signup
Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "created_at": "2024-01-10T12:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Account created successfully"
}
```

#### POST /api/auth/signin
Authenticate an existing user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "created_at": "2024-01-10T12:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Signin successful"
}
```

### Health Check

#### GET /health
Check API health status.

**Response:**
```json
{
  "status": "healthy"
}
```

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number

## Security Features

- **JWT Authentication**: Stateless authentication with 24-hour token expiration
- **Password Hashing**: Bcrypt with 12 rounds and automatic salt generation
- **CORS Protection**: Configured to allow only frontend origin
- **Input Validation**: Server-side validation for all user inputs
- **Generic Error Messages**: Prevents user enumeration attacks
- **Protected Routes**: Automatic redirect for unauthenticated users
- **Password Visibility Toggle**: User-friendly password input with show/hide

## Development Workflow

### Running Both Services

You can run both backend and frontend simultaneously in separate terminals:

**Terminal 1 (Backend):**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### Database Migrations

The application automatically creates database tables on startup. No manual migration is needed for initial setup.

## Testing the Application

### Basic Authentication Test
1. **Start both services** (backend and frontend)
2. **Navigate to** `http://localhost:3000`
3. **Click "Get Started"** or "Sign Up"
4. **Create an account** with a valid email and password
5. **Verify redirect** to the tasks page
6. **Sign out** and sign back in to test authentication

### AI Chatbot Test (NEW!)
1. **Navigate to** `http://localhost:3000/chat`
2. **Try these commands:**
   - "Add a todo to buy groceries"
   - "Show me my todos"
   - "Mark todo 1 as complete"
   - "Delete todo 1"
3. **Verify** the AI responds and performs actions
4. **Check** that todos are created/updated/deleted correctly

## Troubleshooting

### Backend Issues

**OpenAI API key error:**
- Add `OPENAI_API_KEY=sk-your-key-here` to `backend/.env`
- Ensure the API key is valid and has credits
- Restart the backend server after adding the key

**Database connection error:**
- Verify `DATABASE_URL` is correct in `backend/.env`
- Ensure PostgreSQL database is accessible
- Check network connectivity to database host

**Missing environment variables:**
- Ensure all required variables are set in `backend/.env`
- Restart the backend server after changing environment variables

### Frontend Issues

**API connection error:**
- Verify `NEXT_PUBLIC_API_URL` is correct in `frontend/.env.local`
- Ensure backend is running on the specified port
- Check browser console for CORS errors

**Build errors:**
- Delete `node_modules` and `.next` folders
- Run `npm install` again
- Ensure Node.js version is 18+

## Contributing

This project follows spec-driven development using GitHub Spec-Kit:

1. Read the feature spec in `/specs/002-landing-auth/spec.md`
2. Review the implementation plan in `/specs/002-landing-auth/plan.md`
3. Follow the task breakdown in `/specs/002-landing-auth/tasks.md`
4. Update specs if requirements change

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ for Hackathon II
