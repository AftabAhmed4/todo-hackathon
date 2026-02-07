# AI Todo Chatbot - Quickstart Guide

**Feature**: 002-ai-todo-chatbot
**Date**: 2026-02-05
**Purpose**: Quick setup and usage guide for developers

## Overview

The AI Todo Chatbot enables users to manage their todos through natural language conversations. This guide covers setup, development, testing, and usage.

## Prerequisites

### Required Software
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **PostgreSQL**: Neon Serverless PostgreSQL account
- **Git**: For version control

### Required API Keys
- **OpenAI API Key**: For AI agent functionality
  - Sign up at https://platform.openai.com/
  - Create API key in dashboard
  - Ensure sufficient credits for development/testing

### Existing Setup
This feature builds on existing authentication and todo management:
- User authentication (Better Auth) already implemented
- Task CRUD operations already implemented
- Database connection already configured

## Environment Setup

### Backend Environment Variables

Create or update `backend/.env`:

```bash
# Existing variables (keep these)
DATABASE_URL='postgresql://neondb_owner:npg_TAhvS0IXZYu9@ep-ancient-frog-ahufity2-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
BETTER_AUTH_SECRET=Efcv1Frd_q1DUWMYsJDnS_49wYM40NPCx9kVHEhOSCM
API_PORT=8001
ENVIRONMENT=development
FRONTEND_URL=http://localhost:3000

# New variable for AI chatbot
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Important**: Replace `sk-your-openai-api-key-here` with your actual OpenAI API key.

### Frontend Environment Variables

Update `frontend/.env.local`:

```bash
# Existing variables (keep these)
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_ENVIRONMENT=development
```

No new frontend environment variables needed.

## Installation

### Backend Dependencies

```bash
cd backend

# Install new dependencies
pip install openai mcp pydantic

# Or update requirements.txt and install all
pip install -r requirements.txt
```

**New dependencies**:
- `openai`: Official OpenAI Python SDK for AI agent
- `mcp`: Official MCP SDK for tool server
- `pydantic`: For data validation (may already be installed)

### Frontend Dependencies

```bash
cd frontend

# Install new dependencies
npm install react-markdown

# Or install all dependencies
npm install
```

**New dependencies**:
- `react-markdown`: For rendering markdown in chat messages

## Database Migration

### Create New Tables

Run the migration to create `conversations` and `messages` tables:

**Option 1: Using SQLModel (Recommended)**

```bash
cd backend
python -c "from db import create_db_and_tables; create_db_and_tables()"
```

This will create all tables including the new ones.

**Option 2: Using SQL Script**

```bash
# Connect to your Neon database
psql $DATABASE_URL

# Run migration
\i migrations/add_chat_tables.sql
```

### Verify Tables Created

```bash
psql $DATABASE_URL -c "\dt"
```

You should see:
- `users` (existing)
- `tasks` (existing)
- `conversations` (new)
- `messages` (new)

## Running the Application

### Start Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8001
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete.
```

**Verify backend is running**:
```bash
curl http://localhost:8001/health
# Expected: {"status":"healthy"}
```

### Start Frontend Server

```bash
cd frontend
npm run dev
```

**Expected output**:
```
ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

**Verify frontend is running**:
Open http://localhost:3000 in your browser.

## Usage Guide

### 1. Sign In or Sign Up

Navigate to http://localhost:3000 and:
- Sign up with a new account, or
- Sign in with existing credentials

**Note**: If you have authentication issues, use the password reset script:
```bash
cd backend
python reset_password.py
```

### 2. Access Chat Interface

After signing in, navigate to:
- http://localhost:3000/chat

Or click "Chat" in the navigation menu.

### 3. Chat with AI Assistant

**Create a todo**:
```
You: Add a task to buy groceries
AI: I've added 'Buy groceries' to your todo list.
```

**List todos**:
```
You: What are my tasks?
AI: You have 1 task:
1. Buy groceries (pending)
```

**Update todo status**:
```
You: Mark buy groceries as done
AI: Great! I've marked 'Buy groceries' as completed.
```

**Update todo details**:
```
You: Change the grocery task to buy groceries and cook dinner
AI: I've updated the task to 'Buy groceries and cook dinner'.
```

**Delete todo**:
```
You: Delete the grocery task
AI: I've removed 'Buy groceries and cook dinner' from your list.
```

### 4. Multi-turn Conversations

The AI maintains context across messages:

```
You: Add a task to call the dentist
AI: I've added 'Call the dentist' to your todo list.

You: What are my tasks?
AI: You have 1 task:
1. Call the dentist (pending)

You: Mark the first one as done
AI: Great! I've marked 'Call the dentist' as completed.
```

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_chat.py

# Run with coverage
pytest --cov=. --cov-report=html
```

**Test categories**:
- Unit tests: Individual MCP tools, AI agent functions
- Integration tests: /api/chat endpoint, database operations
- Contract tests: API response schemas

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run specific test
npm test ChatInterface

# Run with coverage
npm test -- --coverage
```

**Test categories**:
- Component tests: ChatInterface, MessageList, MessageInput
- Integration tests: API client, chat flow

### Manual Testing Checklist

- [ ] Sign up new user
- [ ] Sign in existing user
- [ ] Navigate to chat page
- [ ] Send first message (creates conversation)
- [ ] Create todo via chat
- [ ] List todos via chat
- [ ] Update todo status via chat
- [ ] Update todo details via chat
- [ ] Delete todo via chat
- [ ] Multi-turn conversation with context
- [ ] Error handling (invalid input, network errors)
- [ ] Sign out and verify conversation persists on sign in

## Development Workflow

### Making Changes

1. **Backend changes**:
   - Edit files in `backend/`
   - Server auto-reloads with `--reload` flag
   - Test changes with curl or frontend

2. **Frontend changes**:
   - Edit files in `frontend/`
   - Browser auto-refreshes with hot reload
   - Test changes in browser

3. **Database changes**:
   - Update models in `backend/models.py`
   - Create migration script
   - Run migration
   - Update schemas in `backend/schemas.py`

### Debugging

**Backend debugging**:
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uvicorn main:app --reload --port 8001
```

**Check logs**:
- Backend logs appear in terminal
- Look for AI agent invocations, tool selections, database queries

**Frontend debugging**:
- Open browser DevTools (F12)
- Check Console tab for errors
- Check Network tab for API requests
- Use React DevTools for component inspection

### Common Issues

**Issue**: "OpenAI API key not found"
**Solution**: Ensure `OPENAI_API_KEY` is set in `backend/.env`

**Issue**: "Conversation not found"
**Solution**: Check that conversation_id belongs to authenticated user

**Issue**: "AI not understanding intent"
**Solution**: Check system prompt in `backend/services/ai_agent.py`, add more examples

**Issue**: "Database connection error"
**Solution**: Verify `DATABASE_URL` is correct and database is accessible

**Issue**: "CORS error in browser"
**Solution**: Verify `FRONTEND_URL` in backend `.env` matches frontend URL

## API Endpoints

### Chat Endpoints

**Send message**:
```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy milk"}'
```

**List conversations**:
```bash
curl http://localhost:8001/api/conversations \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Get conversation history**:
```bash
curl http://localhost:8001/api/conversations/123 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Existing Endpoints

**Sign up**:
```bash
curl -X POST http://localhost:8001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Test1234"}'
```

**Sign in**:
```bash
curl -X POST http://localhost:8001/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Test1234"}'
```

## Performance Optimization

### Backend Optimization

1. **Limit conversation history**:
   - Load only last 20 messages by default
   - Configurable in `backend/routes/chat.py`

2. **Database connection pooling**:
   - Already configured in `backend/db.py`
   - Adjust pool size if needed

3. **Cache AI agent configuration**:
   - Initialize OpenAI client once
   - Reuse across requests

### Frontend Optimization

1. **Lazy load old messages**:
   - Load recent messages first
   - Fetch older messages on scroll

2. **Debounce user input**:
   - Prevent rapid-fire requests
   - Show typing indicator

3. **Optimize re-renders**:
   - Use React.memo for message components
   - Implement virtual scrolling for long conversations

## Monitoring

### Key Metrics to Track

1. **Chat request volume**: Requests per minute
2. **AI service latency**: Time to get AI response
3. **Database query performance**: Query execution time
4. **Error rates**: Failed requests by type
5. **OpenAI API costs**: Token usage and costs

### Logging

**Backend logs include**:
- Chat request received (user_id, conversation_id)
- AI agent invoked (model, token count)
- MCP tool selected (tool name, arguments)
- Tool execution result (success/error)
- Response sent (latency)

**Log levels**:
- INFO: Normal operations
- WARNING: Recoverable errors
- ERROR: Failed requests
- DEBUG: Detailed execution flow

## Cost Estimation

### OpenAI API Costs

**Assumptions**:
- Average 10 messages per conversation
- Average 100 tokens per message
- Using GPT-4 Turbo

**Cost per conversation**:
- Input: 10 messages × 100 tokens × $0.01/1k = $0.10
- Output: 10 responses × 50 tokens × $0.03/1k = $0.015
- **Total**: ~$0.12 per conversation

**Monthly costs** (1000 users, 5 conversations each):
- 5000 conversations × $0.12 = **$600/month**

**Cost optimization**:
- Use GPT-3.5 Turbo for simple operations (10x cheaper)
- Implement response caching
- Limit conversation history length

## Security Considerations

1. **Authentication**: All chat endpoints require JWT token
2. **Authorization**: Users can only access their own conversations
3. **Input validation**: Message length limits, SQL injection prevention
4. **API key security**: OpenAI key stored in environment variable
5. **Rate limiting**: Consider implementing rate limits for production

## Next Steps

After completing quickstart setup:

1. **Explore the codebase**:
   - Review `backend/routes/chat.py` for chat endpoint
   - Review `backend/services/ai_agent.py` for AI logic
   - Review `frontend/components/ChatInterface.tsx` for UI

2. **Run tests**:
   - Execute backend and frontend test suites
   - Verify all tests pass

3. **Experiment with AI**:
   - Try different natural language inputs
   - Test edge cases and error handling
   - Refine system prompt for better accuracy

4. **Read documentation**:
   - Review `specs/002-ai-todo-chatbot/plan.md` for architecture
   - Review `specs/002-ai-todo-chatbot/data-model.md` for database schema
   - Review API contracts in `specs/002-ai-todo-chatbot/contracts/`

## Support

**Issues or questions?**
- Check existing documentation in `specs/002-ai-todo-chatbot/`
- Review error logs in terminal
- Test with curl to isolate frontend vs backend issues

**Common resources**:
- OpenAI API docs: https://platform.openai.com/docs
- MCP SDK docs: https://modelcontextprotocol.io/
- FastAPI docs: https://fastapi.tiangolo.com/
- Next.js docs: https://nextjs.org/docs

---

**Quickstart Status**: Complete
**Ready for**: Development and testing
**Estimated setup time**: 15-30 minutes
