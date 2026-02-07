# Implementation Plan: AI Todo Chatbot

**Branch**: `002-ai-todo-chatbot` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-ai-todo-chatbot/spec.md`

## Summary

Build an AI-powered conversational Todo chatbot that enables users to manage their todos through natural language interactions. The system uses MCP (Model Context Protocol) server architecture with stateless components: an OpenAI AI agent interprets user intent, selects appropriate MCP tools (create_todo, list_todos, update_todo, delete_todo, complete_todo), and executes database operations. All conversation state is persisted in the database and loaded per request to maintain stateless architecture. The frontend uses OpenAI ChatKit for a chat-only interface, connecting to a FastAPI /chat endpoint that orchestrates the AI agent and MCP tools.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/JavaScript (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, OpenAI Agents SDK, Official MCP SDK, Better Auth, python-jose, passlib
- Frontend: Next.js 14, OpenAI ChatKit, React, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL (existing + new tables: conversations, messages)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (Linux server backend, browser frontend)
**Project Type**: Web (frontend + backend monorepo)
**Performance Goals**:
- 3-second response time for 95% of chat requests
- Support 100 concurrent users
- Handle conversations up to 50 messages without degradation
**Constraints**:
- All components must be stateless (no in-memory state)
- Conversation context loaded from database per request
- MCP tools perform database operations only
- Chat-only interface (no form-based UI)
**Scale/Scope**:
- Expected 10-100 users initially
- 10-100 todos per user average
- 5-20 messages per conversation typical

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Required Gate Verification

- [x] **Spec-Driven Workflow**: Feature implementation follows Spec-Kit Plus → Claude Code → Tasks → Implementation workflow. No manual coding.
- [x] **Database Isolation**: All database operations use SQLModel with user-scoped queries via foreign key. No direct frontend-to-database access.
- [x] **JWT Authentication**: All API endpoints secured with JWT tokens. Better Auth issues tokens, backend verifies using BETTER_AUTH_SECRET.
- [x] **API Contract**: New /api/chat endpoint follows RESTful patterns. Existing /api/{user_id}/tasks/* endpoints remain unchanged.
- [x] **Frontend Auth State**: Frontend handles auth state, API client automatically attaches JWT tokens. UI reflects only authenticated user data.
- [x] **Monorepo Structure**: Implementation fits in frontend/ and backend/ folders. Spec-Kit files at root or /specs.
- [x] **No Hardcoded Secrets**: All secrets (BETTER_AUTH_SECRET, OPENAI_API_KEY, DATABASE_URL) via environment variables.
- [x] **Production Quality**: Code is reviewable, production-grade. No placeholder logic, mock auth, or insecure shortcuts.

### Complexity Tracking Justification

No violations - all requirements align with constitution principles.

## Project Structure

### Documentation (this feature)

```text
specs/002-ai-todo-chatbot/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (MCP SDK, OpenAI Agents SDK research)
├── data-model.md        # Phase 1 output (Conversation, Message models)
├── contracts/           # Phase 1 output (API contracts)
│   ├── chat-api.yaml    # /api/chat endpoint contract
│   └── mcp-tools.yaml   # MCP tool schemas
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── models.py            # Existing: User, Task | New: Conversation, Message
├── routes/
│   ├── auth.py          # Existing authentication routes
│   ├── tasks.py         # Existing task CRUD routes
│   └── chat.py          # NEW: Chat endpoint
├── services/
│   ├── ai_agent.py      # NEW: OpenAI Agent integration
│   └── mcp_server.py    # NEW: MCP server with tools
├── schemas.py           # Existing + new chat request/response schemas
├── db.py                # Existing database connection
├── auth.py              # Existing JWT authentication
├── main.py              # Existing FastAPI app (add chat router)
└── requirements.txt     # Add: openai-agents-sdk, mcp-sdk

frontend/
├── app/
│   ├── chat/
│   │   └── page.tsx     # NEW: Chat interface page
│   ├── tasks/
│   │   └── page.tsx     # Existing tasks page (keep for reference)
│   ├── signin/          # Existing
│   └── signup/          # Existing
├── components/
│   ├── ChatInterface.tsx # NEW: OpenAI ChatKit wrapper
│   └── Header.tsx       # Existing (add chat navigation)
├── lib/
│   ├── api.ts           # Existing (add chat methods)
│   ├── auth.tsx         # Existing
│   └── types.ts         # Existing + new chat types
└── package.json         # Add: @openai/chatkit

mcp-server/              # NEW: Standalone MCP server directory
├── server.py            # MCP server entry point
├── tools/
│   ├── create_todo.py
│   ├── list_todos.py
│   ├── update_todo.py
│   ├── delete_todo.py
│   └── complete_todo.py
└── schemas.py           # Tool input/output schemas
```

**Structure Decision**: Web application structure (Option 2) with existing backend/ and frontend/ folders. New mcp-server/ directory for MCP tools to maintain separation of concerns. The MCP server will be integrated with the FastAPI backend but organized separately for clarity.

## Phase 0: Research & Discovery

### Research Objectives

1. **MCP SDK Investigation**
   - Research Official MCP SDK documentation and examples
   - Understand MCP protocol for tool definition and invocation
   - Identify how to create stateless MCP tools in Python
   - Determine MCP server integration with FastAPI
   - Document tool schema definition patterns

2. **OpenAI Agents SDK Investigation**
   - Research OpenAI Agents SDK architecture and capabilities
   - Understand stateless agent configuration
   - Identify how agents select and invoke MCP tools
   - Determine conversation context passing mechanisms
   - Document agent prompt engineering best practices

3. **OpenAI ChatKit Investigation**
   - Research OpenAI ChatKit React components
   - Understand chat UI customization options
   - Identify integration patterns with custom backends
   - Determine message formatting and display options
   - Document authentication integration

4. **Stateless Architecture Patterns**
   - Research best practices for stateless conversational AI
   - Identify conversation history management patterns
   - Understand context window optimization
   - Document database schema patterns for chat history

### Research Deliverables

Create `specs/002-ai-todo-chatbot/research.md` with:
- MCP SDK setup and tool creation guide
- OpenAI Agents SDK configuration patterns
- OpenAI ChatKit integration examples
- Stateless architecture decision rationale
- Code examples and references

## Phase 1: Architecture & Design

### 1.1 System Architecture

**Overall Flow**:
```
User → ChatKit UI → /api/chat endpoint → AI Agent → MCP Tools → Database
                         ↓                    ↑
                    Load conversation    Return results
                    history from DB
```

**Component Boundaries**:

1. **AI Reasoning Layer** (OpenAI Agent)
   - Interprets natural language user input
   - Identifies user intent (create, list, update, delete, complete)
   - Selects appropriate MCP tool
   - Formats tool arguments from natural language
   - Generates conversational responses
   - **Stateless**: Receives conversation history as input, no internal state

2. **MCP Tool Execution Layer** (MCP Server)
   - Exposes 5 stateless tools: create_todo, list_todos, update_todo, delete_todo, complete_todo
   - Validates tool input schemas
   - Executes database operations via SQLModel
   - Returns structured results
   - **Stateless**: Each tool invocation is independent, no shared state

3. **Data Persistence Layer** (PostgreSQL + SQLModel)
   - Stores users, todos, conversations, messages
   - Enforces user-scoped data access via foreign keys
   - Maintains referential integrity
   - Provides conversation history for context loading

4. **API Orchestration Layer** (FastAPI /chat endpoint)
   - Authenticates requests via JWT
   - Loads conversation history from database
   - Passes context to AI agent
   - Persists user message and agent response
   - Returns response to frontend
   - **Stateless**: Each request is independent

### 1.2 Data Model Design

Create `specs/002-ai-todo-chatbot/data-model.md` with:

**New Models**:

```python
# Conversation Model
class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: Optional[str] = Field(default=None, max_length=200)  # Auto-generated from first message
    created_at: datetime
    updated_at: datetime

# Message Model
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str = Field(max_length=10000)
    created_at: datetime
```

**Existing Models** (no changes):
- User: id, email, password_hash, created_at, updated_at
- Task: id, user_id, title, description, status, created_at, updated_at

**Relationships**:
- User → Conversations (one-to-many)
- User → Tasks (one-to-many)
- Conversation → Messages (one-to-many)
- Messages reference Conversation via conversation_id
- All queries enforce user_id scoping

**Indexes**:
- conversations.user_id (for user's conversation list)
- messages.conversation_id (for loading conversation history)
- messages.created_at (for chronological ordering)

### 1.3 API Contracts

Create `specs/002-ai-todo-chatbot/contracts/chat-api.yaml`:

```yaml
/api/chat:
  post:
    summary: Send message to AI chatbot
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - message
            properties:
              message:
                type: string
                description: User's natural language message
              conversation_id:
                type: integer
                description: Existing conversation ID (optional for new conversation)
    responses:
      200:
        description: AI response
        content:
          application/json:
            schema:
              type: object
              properties:
                conversation_id:
                  type: integer
                response:
                  type: string
                  description: AI agent's natural language response
                created_at:
                  type: string
                  format: date-time
      401:
        description: Unauthorized
      500:
        description: Server error
```

Create `specs/002-ai-todo-chatbot/contracts/mcp-tools.yaml`:

```yaml
tools:
  create_todo:
    input:
      type: object
      required: [user_id, title]
      properties:
        user_id: {type: integer}
        title: {type: string, maxLength: 500}
        description: {type: string, maxLength: 2000}
        status: {type: string, enum: [pending, in_progress, completed]}
    output:
      type: object
      properties:
        id: {type: integer}
        title: {type: string}
        status: {type: string}
        created_at: {type: string, format: date-time}

  list_todos:
    input:
      type: object
      required: [user_id]
      properties:
        user_id: {type: integer}
        status: {type: string, enum: [pending, in_progress, completed]}
    output:
      type: array
      items:
        type: object
        properties:
          id: {type: integer}
          title: {type: string}
          description: {type: string}
          status: {type: string}
          created_at: {type: string}

  update_todo:
    input:
      type: object
      required: [user_id, todo_id]
      properties:
        user_id: {type: integer}
        todo_id: {type: integer}
        title: {type: string}
        description: {type: string}
        status: {type: string}
    output:
      type: object
      properties:
        id: {type: integer}
        title: {type: string}
        status: {type: string}
        updated_at: {type: string}

  delete_todo:
    input:
      type: object
      required: [user_id, todo_id]
      properties:
        user_id: {type: integer}
        todo_id: {type: integer}
    output:
      type: object
      properties:
        success: {type: boolean}
        message: {type: string}

  complete_todo:
    input:
      type: object
      required: [user_id, todo_id]
      properties:
        user_id: {type: integer}
        todo_id: {type: integer}
    output:
      type: object
      properties:
        id: {type: integer}
        status: {type: string}
        updated_at: {type: string}
```

### 1.4 Quickstart Guide

Create `specs/002-ai-todo-chatbot/quickstart.md`:

```markdown
# AI Todo Chatbot - Quickstart Guide

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (Neon)
- OpenAI API key

## Environment Setup

### Backend (.env)
```
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret
OPENAI_API_KEY=your-openai-key
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## Installation

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8001
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Sign up or sign in at http://localhost:3000
2. Navigate to /chat
3. Start chatting: "Add a task to buy groceries"
4. View tasks: "What are my tasks?"
5. Complete tasks: "Mark buy groceries as done"

## Testing

### Backend
```bash
cd backend
pytest tests/
```

### Frontend
```bash
cd frontend
npm test
```
```

## Phase 2: MCP Server Implementation

### 2.1 MCP Server Setup

**File**: `mcp-server/server.py`

- Initialize MCP server using Official MCP SDK
- Register 5 tools: create_todo, list_todos, update_todo, delete_todo, complete_todo
- Configure database connection (reuse backend/db.py patterns)
- Implement tool discovery endpoint
- Ensure stateless operation (no global state)

### 2.2 MCP Tool Implementation

**Files**: `mcp-server/tools/*.py`

Each tool must:
1. Define input schema (Pydantic model)
2. Validate user_id authorization
3. Execute database operation via SQLModel
4. Return structured output
5. Handle errors gracefully
6. Log operations for debugging

**create_todo**:
- Input: user_id, title, description (optional), status (default: pending)
- Validate: title not empty, user_id exists
- Operation: Insert new Task record
- Output: Created task with id, title, status, created_at

**list_todos**:
- Input: user_id, status (optional filter)
- Validate: user_id exists
- Operation: Query tasks WHERE user_id = ? [AND status = ?]
- Output: Array of tasks with all fields

**update_todo**:
- Input: user_id, todo_id, title (optional), description (optional), status (optional)
- Validate: todo belongs to user
- Operation: Update task fields, set updated_at
- Output: Updated task

**delete_todo**:
- Input: user_id, todo_id
- Validate: todo belongs to user
- Operation: DELETE task WHERE id = ? AND user_id = ?
- Output: Success confirmation

**complete_todo**:
- Input: user_id, todo_id
- Validate: todo belongs to user
- Operation: UPDATE task SET status = 'completed', updated_at = NOW()
- Output: Updated task with new status

### 2.3 Tool Schema Definitions

**File**: `mcp-server/schemas.py`

Define Pydantic models for:
- CreateTodoInput, CreateTodoOutput
- ListTodosInput, ListTodosOutput
- UpdateTodoInput, UpdateTodoOutput
- DeleteTodoInput, DeleteTodoOutput
- CompleteTodoInput, CompleteTodoOutput

## Phase 3: AI Agent Implementation

### 3.1 Agent Configuration

**File**: `backend/services/ai_agent.py`

- Initialize OpenAI Agent with API key
- Configure agent with system prompt:
  ```
  You are a helpful todo management assistant. You help users create, view, update, and delete their todos through natural conversation. When users describe tasks in natural language, extract the key information and use the appropriate tool. Always respond in a friendly, conversational tone.
  ```
- Register MCP tools with agent
- Implement stateless agent invocation:
  - Accept conversation history as input
  - Return agent response
  - No internal state storage

### 3.2 Intent Recognition

Agent must identify user intent from natural language:
- **Create**: "Add task", "Remind me to", "I need to", "Create a todo"
- **List**: "Show my tasks", "What do I need to do", "List todos"
- **Update**: "Change task", "Update the", "Modify"
- **Delete**: "Remove task", "Delete the", "Get rid of"
- **Complete**: "Mark as done", "I finished", "Complete the"

### 3.3 Tool Selection Logic

Agent selects appropriate MCP tool based on intent:
1. Parse user message
2. Identify primary intent
3. Extract relevant parameters (todo title, id, status)
4. Select matching tool
5. Format tool arguments
6. Invoke tool
7. Format tool result into natural language response

### 3.4 Context Management

- Agent receives full conversation history (last N messages)
- Uses context to resolve ambiguous references ("the first one", "that task")
- Maintains conversational flow across multiple turns
- No state stored in agent - all context from database

## Phase 4: Chat API Implementation

### 4.1 Chat Endpoint

**File**: `backend/routes/chat.py`

```python
@router.post("/api/chat")
async def chat(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user)
):
    # 1. Get or create conversation
    # 2. Load conversation history from database
    # 3. Append user message to history
    # 4. Persist user message
    # 5. Invoke AI agent with history
    # 6. Persist agent response
    # 7. Return response to frontend
```

### 4.2 Conversation Management

- If conversation_id provided: Load existing conversation
- If no conversation_id: Create new conversation
- Validate user owns conversation
- Load last 20 messages for context (configurable)
- Auto-generate conversation title from first user message

### 4.3 Message Persistence

- Persist user message immediately after receiving
- Persist agent response after generation
- Include timestamps for all messages
- Maintain message order via created_at

### 4.4 Error Handling

- Handle AI service errors (rate limits, timeouts)
- Handle database errors
- Handle invalid conversation_id
- Return user-friendly error messages
- Log errors for debugging

## Phase 5: Database Schema Updates

### 5.1 Migration Script

**File**: `backend/migrations/add_chat_tables.py`

```python
# Create conversations table
# Create messages table
# Add indexes
# Add foreign key constraints
```

### 5.2 Model Updates

**File**: `backend/models.py`

- Add Conversation model
- Add Message model
- Ensure compatibility with existing User and Task models

### 5.3 Database Initialization

Update `backend/db.py`:
- Include new models in create_db_and_tables()
- Verify foreign key constraints
- Test user-scoped queries

## Phase 6: Frontend Implementation

### 6.1 Chat Interface Page

**File**: `frontend/app/chat/page.tsx`

- Create chat page route
- Implement authentication check
- Render ChatInterface component
- Handle loading states
- Display errors

### 6.2 ChatInterface Component

**File**: `frontend/components/ChatInterface.tsx`

- Integrate OpenAI ChatKit
- Connect to /api/chat endpoint
- Display message history
- Handle user input
- Show typing indicators
- Format AI responses
- Handle errors gracefully

### 6.3 API Client Updates

**File**: `frontend/lib/api.ts`

Add chat methods:
```typescript
async sendMessage(message: string, conversationId?: number): Promise<ChatResponse>
async getConversations(): Promise<Conversation[]>
```

### 6.4 Type Definitions

**File**: `frontend/lib/types.ts`

```typescript
interface ChatRequest {
  message: string;
  conversation_id?: number;
}

interface ChatResponse {
  conversation_id: number;
  response: string;
  created_at: string;
}

interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}
```

### 6.5 Navigation Updates

**File**: `frontend/components/Header.tsx`

- Add "Chat" navigation link
- Highlight active route
- Maintain existing navigation items

## Phase 7: Authentication & Authorization

### 7.1 Chat Endpoint Security

- Apply `Depends(get_current_user)` to /api/chat
- Verify JWT token on every request
- Extract user_id from token
- Pass user_id to AI agent and MCP tools

### 7.2 Conversation Ownership

- Validate user owns conversation before loading
- Return 403 if user tries to access another user's conversation
- Ensure all MCP tools receive and validate user_id

### 7.3 Frontend Auth Integration

- Reuse existing auth context
- Attach JWT token to chat API requests
- Redirect to signin if unauthenticated
- Handle 401 responses

## Phase 8: Error Handling & Validation

### 8.1 Input Validation

**Backend**:
- Validate message length (max 1000 characters)
- Validate conversation_id exists and belongs to user
- Validate MCP tool inputs via Pydantic schemas

**Frontend**:
- Prevent empty message submission
- Show character count for long messages
- Validate before sending to backend

### 8.2 Error Scenarios

**AI Service Errors**:
- Rate limit exceeded: "I'm receiving too many requests. Please try again in a moment."
- Timeout: "I'm taking longer than expected. Please try again."
- API error: "I'm having trouble processing your request. Please try again."

**Database Errors**:
- Connection failure: "Unable to save your message. Please check your connection."
- Query error: "Something went wrong. Please try again."

**Invalid Input**:
- Ambiguous request: "I'm not sure what you'd like me to do. Could you be more specific?"
- Missing todo reference: "I couldn't find that task. Would you like to see your current tasks?"

### 8.3 Graceful Degradation

- If AI service unavailable: Show error message, allow retry
- If database slow: Show loading indicator, timeout after 10 seconds
- If MCP tool fails: Agent explains error in natural language

### 8.4 Logging & Monitoring

- Log all chat requests with user_id, conversation_id
- Log AI agent invocations and tool selections
- Log MCP tool executions and results
- Log errors with stack traces
- Monitor response times and error rates

## Phase 9: Testing Strategy

### 9.1 Backend Tests

**Unit Tests** (`backend/tests/unit/`):
- Test each MCP tool independently
- Test AI agent tool selection logic
- Test conversation management functions
- Test message persistence

**Integration Tests** (`backend/tests/integration/`):
- Test /api/chat endpoint end-to-end
- Test AI agent + MCP tool integration
- Test database operations
- Test authentication flow

**Contract Tests** (`backend/tests/contract/`):
- Verify /api/chat matches contract
- Verify MCP tool schemas match contract

### 9.2 Frontend Tests

**Component Tests** (`frontend/tests/components/`):
- Test ChatInterface rendering
- Test message display
- Test user input handling
- Test error states

**Integration Tests** (`frontend/tests/integration/`):
- Test chat flow end-to-end
- Test API client methods
- Test authentication integration

### 9.3 End-to-End Tests

**User Scenarios**:
- Create todo via chat
- List todos via chat
- Update todo status via chat
- Delete todo via chat
- Multi-turn conversation with context

## Phase 10: Deployment Considerations

### 10.1 Environment Variables

**Backend**:
- DATABASE_URL (Neon PostgreSQL)
- BETTER_AUTH_SECRET (JWT signing)
- OPENAI_API_KEY (AI agent)
- FRONTEND_URL (CORS)

**Frontend**:
- NEXT_PUBLIC_API_URL (backend endpoint)

### 10.2 Database Migrations

- Run migration script to create conversations and messages tables
- Verify indexes created
- Test user-scoped queries

### 10.3 Dependency Installation

**Backend**:
```bash
pip install openai-agents-sdk mcp-sdk
```

**Frontend**:
```bash
npm install @openai/chatkit
```

### 10.4 Performance Optimization

- Limit conversation history to last 20 messages
- Add database indexes for common queries
- Cache AI agent configuration
- Implement request timeout (10 seconds)

### 10.5 Monitoring

- Track chat request volume
- Monitor AI service API usage and costs
- Track error rates by type
- Monitor database query performance

## Success Criteria Verification

After implementation, verify:

1. **SC-001**: Users can create a todo in under 10 seconds
   - Test: Send "Add task to buy milk" → Verify todo created within 10s

2. **SC-002**: 90% intent interpretation accuracy
   - Test: 100 sample messages → Verify 90+ correct tool selections

3. **SC-003**: Full workflow via chat only
   - Test: Create, view, update, delete todo without forms

4. **SC-004**: Context maintained across 10 messages
   - Test: 10-message conversation with references → Verify context preserved

5. **SC-005**: 3-second response time for 95% of requests
   - Test: 100 requests → Verify 95+ respond within 3s

6. **SC-006**: 100 concurrent users
   - Load test: Simulate 100 concurrent chat sessions

7. **SC-007**: 85% first-time success rate
   - Test: 20 new users → Verify 17+ create first todo successfully

8. **SC-008**: 100% conversation persistence
   - Test: All conversations and messages saved to database

9. **SC-009**: Stateless architecture verified
   - Test: Restart services mid-conversation → Verify context preserved

10. **SC-010**: Zero unauthorized access
    - Security test: Attempt cross-user access → Verify all blocked

## Risk Mitigation

### Technical Risks

1. **MCP SDK Maturity**: If SDK is unstable or poorly documented
   - Mitigation: Research thoroughly in Phase 0, consider alternative tool frameworks

2. **OpenAI Agents SDK Limitations**: If SDK doesn't support stateless architecture
   - Mitigation: Implement custom agent wrapper, use OpenAI API directly if needed

3. **AI Service Costs**: OpenAI API usage may be expensive
   - Mitigation: Implement request caching, optimize prompts, set usage limits

4. **Context Window Limits**: Long conversations may exceed AI context limits
   - Mitigation: Implement smart context truncation, summarize old messages

### Implementation Risks

1. **Stateless Architecture Complexity**: Managing state in database adds latency
   - Mitigation: Optimize database queries, add indexes, implement caching

2. **Natural Language Ambiguity**: AI may misinterpret user intent
   - Mitigation: Implement clarification prompts, provide examples, allow corrections

3. **Integration Complexity**: Multiple new technologies (MCP, OpenAI Agents, ChatKit)
   - Mitigation: Implement incrementally, test each component independently

## Next Steps

1. **Complete Phase 0 Research**: Create research.md with MCP SDK, OpenAI Agents SDK, and ChatKit findings
2. **Complete Phase 1 Design**: Create data-model.md, contracts/, and quickstart.md
3. **Run `/sp.tasks`**: Generate detailed task breakdown from this plan
4. **Begin Implementation**: Follow Agentic Dev Stack workflow (Spec → Plan → Tasks → Implement)

---

**Plan Status**: Ready for task generation via `/sp.tasks`
**Estimated Complexity**: High (new architecture patterns, multiple new technologies)
**Estimated Timeline**: 2-3 weeks for full implementation and testing
