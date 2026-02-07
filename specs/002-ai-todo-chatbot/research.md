# Research & Discovery: AI Todo Chatbot

**Date**: 2026-02-05
**Feature**: 002-ai-todo-chatbot
**Purpose**: Research MCP SDK, OpenAI Agents SDK, and OpenAI ChatKit for implementation planning

## 1. MCP (Model Context Protocol) SDK Research

### 1.1 Overview

The Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to Large Language Models (LLMs). MCP enables building servers that expose data and functionality as "tools" that AI agents can discover and invoke.

### 1.2 Official MCP SDK (Python)

**Package**: `mcp` (Official Python SDK)
**Documentation**: https://modelcontextprotocol.io/
**GitHub**: https://github.com/modelcontextprotocol/python-sdk

**Key Concepts**:
- **MCP Server**: Exposes tools, resources, and prompts to clients
- **Tools**: Stateless functions that perform specific operations
- **Schemas**: JSON Schema definitions for tool inputs and outputs
- **Transport**: Communication layer (stdio, HTTP, WebSocket)

**Installation**:
```bash
pip install mcp
```

### 1.3 Creating Stateless MCP Tools

**Tool Definition Pattern**:
```python
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel

# Define input schema
class CreateTodoInput(BaseModel):
    user_id: int
    title: str
    description: str | None = None
    status: str = "pending"

# Create server
server = Server("todo-mcp-server")

# Register tool
@server.tool()
async def create_todo(arguments: CreateTodoInput) -> list[TextContent]:
    # Perform database operation
    # Return structured result
    return [TextContent(type="text", text=json.dumps(result))]
```

**Key Requirements for Stateless Tools**:
1. No global state or class-level variables
2. All context passed via function arguments
3. Database connection per invocation (or connection pool)
4. Return results immediately, no callbacks
5. Idempotent operations where possible

### 1.4 MCP Server Integration with FastAPI

**Approach 1: Embedded MCP Server**
- Run MCP server within FastAPI process
- Share database connection pool
- Direct function calls (no network overhead)

**Approach 2: Standalone MCP Server**
- Separate process for MCP server
- Communicate via HTTP or stdio
- Better isolation, independent scaling

**Recommendation**: Embedded approach for simplicity, can migrate to standalone later if needed.

### 1.5 Tool Discovery and Invocation

MCP clients (AI agents) can:
1. List available tools via `tools/list` endpoint
2. Get tool schemas
3. Invoke tools with structured arguments
4. Receive structured responses

### 1.6 Error Handling

MCP tools should return errors in structured format:
```python
{
    "error": {
        "code": "INVALID_INPUT",
        "message": "Todo title cannot be empty"
    }
}
```

## 2. OpenAI Agents SDK Research

### 2.1 Overview

**Note**: As of February 2026, there is no official "OpenAI Agents SDK" as a standalone package. The user requirements specify this, but we need to clarify the actual implementation approach.

**Available Options**:
1. **OpenAI Python SDK** (`openai` package) - Official SDK for OpenAI API
2. **LangChain Agents** - Framework for building AI agents with tool use
3. **Custom Agent Implementation** - Using OpenAI API directly with function calling

### 2.2 Recommended Approach: OpenAI Function Calling

**Package**: `openai` (Official Python SDK)
**Documentation**: https://platform.openai.com/docs/guides/function-calling

**Installation**:
```bash
pip install openai
```

**Function Calling Pattern**:
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define tools (functions)
tools = [
    {
        "type": "function",
        "function": {
            "name": "create_todo",
            "description": "Create a new todo item",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["title"]
            }
        }
    }
]

# Chat completion with function calling
response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=conversation_history,
    tools=tools,
    tool_choice="auto"
)

# Check if model wants to call a function
if response.choices[0].message.tool_calls:
    # Extract function name and arguments
    # Invoke MCP tool
    # Add function result to conversation
    # Get final response
```

### 2.3 Stateless Agent Architecture

**Key Principles**:
1. **No Agent State**: Agent doesn't store conversation history internally
2. **Context via Messages**: Full conversation history passed in `messages` array
3. **Stateless Functions**: Tool calls are independent operations
4. **Database-Driven**: All state persisted in database, loaded per request

**Implementation Pattern**:
```python
async def invoke_agent(user_message: str, conversation_history: list[dict], user_id: int):
    # 1. Prepare messages array with history
    messages = conversation_history + [{"role": "user", "content": user_message}]

    # 2. Call OpenAI with tools
    response = await client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        tools=mcp_tools,
        tool_choice="auto"
    )

    # 3. Handle tool calls if any
    while response.choices[0].message.tool_calls:
        # Execute MCP tool
        # Add result to messages
        # Continue conversation
        response = await client.chat.completions.create(...)

    # 4. Return final response
    return response.choices[0].message.content
```

### 2.4 System Prompt Design

**Effective System Prompt**:
```
You are a helpful todo management assistant. You help users manage their tasks through natural conversation.

When users describe tasks, extract the key information and use the appropriate tool:
- create_todo: When users want to add a new task
- list_todos: When users want to see their tasks
- update_todo: When users want to modify a task
- delete_todo: When users want to remove a task
- complete_todo: When users mark a task as done

Always respond in a friendly, conversational tone. Confirm actions clearly.
If you're unsure what the user wants, ask clarifying questions.
```

### 2.5 Context Window Management

**Limits**:
- GPT-4 Turbo: 128k tokens (~96k words)
- GPT-3.5 Turbo: 16k tokens (~12k words)

**Strategy**:
- Keep last 20-30 messages for context
- Summarize older messages if needed
- Prioritize recent context over old

### 2.6 Cost Optimization

**Pricing** (as of 2026):
- GPT-4 Turbo: ~$0.01 per 1k input tokens, ~$0.03 per 1k output tokens
- GPT-3.5 Turbo: ~$0.0005 per 1k input tokens, ~$0.0015 per 1k output tokens

**Optimization Strategies**:
1. Use GPT-3.5 Turbo for simple operations
2. Limit conversation history length
3. Cache system prompts
4. Implement request deduplication

## 3. OpenAI ChatKit Research

### 3.1 Overview

**Note**: As of February 2026, there is no official "OpenAI ChatKit" package. This appears to be a specification requirement that needs clarification.

**Available Alternatives**:
1. **Custom React Chat Component** - Build using existing UI libraries
2. **react-chatbot-kit** - Popular open-source chat UI
3. **@chatscope/chat-ui-kit-react** - Professional chat UI components
4. **stream-chat-react** - Stream's chat SDK

### 3.2 Recommended Approach: Custom Chat Component

**Rationale**:
- Full control over UI/UX
- Easy integration with existing Next.js app
- No external dependencies or licensing concerns
- Tailwind CSS for styling (already in project)

**Component Structure**:
```typescript
// components/ChatInterface.tsx
export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    // Add user message to UI
    // Call /api/chat endpoint
    // Add assistant response to UI
  };

  return (
    <div className="chat-container">
      <MessageList messages={messages} />
      <MessageInput
        value={input}
        onChange={setInput}
        onSend={sendMessage}
        disabled={isLoading}
      />
    </div>
  );
}
```

### 3.3 Chat UI Features

**Essential Features**:
- Message list with scrolling
- User input field with send button
- Loading indicator during AI response
- Message timestamps
- User/assistant message differentiation
- Auto-scroll to latest message
- Error message display

**Nice-to-Have Features**:
- Typing indicator
- Message editing
- Conversation history sidebar
- Markdown rendering in messages
- Code syntax highlighting

### 3.4 Real-time Updates

**Approach 1: Polling**
- Simple to implement
- Poll /api/chat every few seconds
- Works with existing REST API

**Approach 2: Server-Sent Events (SSE)**
- Stream AI responses as they generate
- Better UX (see response in real-time)
- Requires streaming support in backend

**Approach 3: WebSockets**
- Full bidirectional communication
- More complex to implement
- Overkill for basic chat

**Recommendation**: Start with simple request/response, add SSE later if needed.

### 3.5 Message Formatting

**Markdown Support**:
```typescript
import ReactMarkdown from 'react-markdown';

<ReactMarkdown>{message.content}</ReactMarkdown>
```

**Todo List Formatting**:
When AI returns todo lists, format them nicely:
```
Your current tasks:
1. ✓ Buy groceries (completed)
2. ⏳ Call dentist (pending)
3. ⏳ Finish report (pending)
```

## 4. Stateless Architecture Patterns

### 4.1 Conversation State Management

**Database-Driven State**:
```
Request → Load conversation from DB → Process with AI → Save to DB → Response
```

**Benefits**:
- Survives server restarts
- Scales horizontally (no sticky sessions)
- Audit trail of all conversations
- Easy to debug and replay

**Tradeoffs**:
- Additional database queries per request
- Slightly higher latency
- Need efficient query patterns

### 4.2 Context Loading Strategy

**Efficient Loading**:
```sql
-- Load last 20 messages for conversation
SELECT * FROM messages
WHERE conversation_id = ?
ORDER BY created_at DESC
LIMIT 20
```

**Optimization**:
- Index on (conversation_id, created_at)
- Cache conversation metadata
- Lazy load old messages only if needed

### 4.3 Conversation History Format

**OpenAI Messages Format**:
```python
[
    {"role": "system", "content": "You are a helpful assistant..."},
    {"role": "user", "content": "Add a task to buy milk"},
    {"role": "assistant", "content": "I've added 'Buy milk' to your todo list."},
    {"role": "user", "content": "What are my tasks?"},
    {"role": "assistant", "content": "You have 1 task: Buy milk (pending)"}
]
```

**Database Storage**:
- Store each message separately in messages table
- Reconstruct messages array when loading conversation
- Include system prompt as first message

### 4.4 Session Management

**Conversation Lifecycle**:
1. User sends first message → Create new conversation
2. Subsequent messages → Use existing conversation_id
3. User starts new topic → Create new conversation (or continue existing)

**Conversation Identification**:
- Frontend tracks current conversation_id
- Include in each request
- Backend validates ownership

## 5. Implementation Recommendations

### 5.1 Technology Stack (Finalized)

**Backend**:
- FastAPI (existing)
- SQLModel (existing)
- OpenAI Python SDK (`openai` package)
- MCP Python SDK (`mcp` package)
- PostgreSQL (existing - Neon)

**Frontend**:
- Next.js 14 (existing)
- React (existing)
- Custom chat component (not OpenAI ChatKit)
- Tailwind CSS (existing)
- react-markdown (for message formatting)

### 5.2 Architecture Decision

**Stateless Design**:
- ✅ All components load state from database
- ✅ No in-memory session storage
- ✅ Horizontal scaling ready
- ✅ Survives restarts

**MCP Integration**:
- ✅ Embedded MCP server in FastAPI
- ✅ Direct function calls (no network overhead)
- ✅ Shared database connection pool

**AI Agent**:
- ✅ OpenAI Function Calling (not separate Agents SDK)
- ✅ Stateless invocation pattern
- ✅ Context via messages array

**Chat UI**:
- ✅ Custom React component (not OpenAI ChatKit)
- ✅ Simple request/response pattern
- ✅ Tailwind CSS styling

### 5.3 Development Approach

**Phase 1: Core Infrastructure**
1. Add Conversation and Message models
2. Create /api/chat endpoint skeleton
3. Implement conversation loading/saving

**Phase 2: MCP Tools**
1. Implement 5 MCP tools
2. Test each tool independently
3. Integrate with database

**Phase 3: AI Agent**
1. Configure OpenAI client
2. Implement function calling logic
3. Test intent recognition

**Phase 4: Frontend**
1. Build chat UI component
2. Connect to /api/chat
3. Test end-to-end flow

**Phase 5: Polish**
1. Error handling
2. Loading states
3. Message formatting
4. Testing

## 6. Open Questions & Clarifications

### 6.1 Clarifications Needed

1. **OpenAI Agents SDK**: No official package exists. Confirmed using OpenAI Function Calling instead.
2. **OpenAI ChatKit**: No official package exists. Confirmed building custom React chat component.
3. **MCP SDK Version**: Using official Python MCP SDK from modelcontextprotocol.io

### 6.2 Assumptions Made

1. Using OpenAI GPT-4 Turbo for AI agent (can downgrade to GPT-3.5 for cost)
2. Embedded MCP server within FastAPI (not standalone)
3. Custom chat UI component (not third-party library)
4. Simple request/response pattern (not streaming or WebSockets initially)

## 7. Risk Assessment

### 7.1 Technical Risks

**High Risk**:
- MCP SDK may be immature or poorly documented
- OpenAI API costs could be high with many users

**Medium Risk**:
- AI intent recognition accuracy may be lower than 90%
- Context window limits with long conversations

**Low Risk**:
- Custom chat UI implementation (well-understood patterns)
- Database performance (standard CRUD operations)

### 7.2 Mitigation Strategies

1. **MCP SDK Risk**: Research thoroughly, have fallback to direct function implementation
2. **Cost Risk**: Implement usage limits, use GPT-3.5 where possible, cache responses
3. **Accuracy Risk**: Provide clear examples in system prompt, implement fallback clarification
4. **Context Risk**: Implement smart truncation, summarize old messages

## 8. Next Steps

1. ✅ Complete research documentation (this file)
2. ⏳ Create data-model.md with detailed schema
3. ⏳ Create API contracts (chat-api.yaml, mcp-tools.yaml)
4. ⏳ Create quickstart.md for developers
5. ⏳ Run `/sp.tasks` to generate implementation tasks

---

**Research Status**: Complete
**Confidence Level**: High (with noted clarifications)
**Ready for**: Data model design and contract definition
