# OpenAI Agents SDK + Gemini API Setup Guide

This guide explains how to use the new OpenAI Agents SDK with Google Gemini API for the todo chatbot.

## 🎯 What Changed

The chatbot now uses:
- **OpenAI Agents SDK** - Professional multi-agent framework
- **Google Gemini via LiteLLM** - Gemini API through LiteLLM adapter
- **Function Tools** - Better tool integration with context support
- **Async Support** - Improved performance with async/await

## 📦 Installation

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `openai-agents==0.7.0` - OpenAI Agents SDK
- `litellm==1.50.0` - LiteLLM for Gemini integration
- All existing dependencies

### 2. Verify Environment Variables

Make sure your `backend/.env` file has:

```env
# Gemini API Key (required)
GEMINI_API_KEY=your_gemini_api_key_here

# Database URL
DATABASE_URL=your_database_url

# JWT Secret
BETTER_AUTH_SECRET=your_secret_key

# CORS
FRONTEND_URL=http://localhost:3000
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

## 🚀 Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

## 🧪 Testing the Chatbot

1. Open browser: http://localhost:3000
2. Sign up or sign in
3. Navigate to `/chat` page
4. Try these commands:

```
"Add a todo to buy groceries"
"Show me all my todos"
"Mark todo 1 as complete"
"Update todo 2 title to 'Call dentist'"
"Delete todo 3"
```

## 🔧 Architecture

### File Structure

```
backend/
├── agent_openai.py          # NEW: OpenAI Agents SDK + Gemini
├── agent.py                  # OLD: Direct Gemini integration (kept for reference)
├── routes/chat.py            # Updated to use agent_openai
├── mcp_tools.py              # MCP tool definitions (still used)
└── requirements.txt          # Updated with new dependencies
```

### How It Works

1. **User sends message** → Frontend → `/api/chat/` endpoint
2. **Chat endpoint** → Loads conversation history from database
3. **Agent execution** → `run_agent_openai()` with user_id context
4. **Gemini via LiteLLM** → Processes message with function calling
5. **Tool execution** → Tools access user_id from context
6. **Response** → Stored in database and returned to frontend

### Key Components

#### 1. LiteLLM Model Configuration

```python
gemini_model = LitellmModel(
    model="gemini/gemini-1.5-pro",
    api_key=api_key,
)
```

#### 2. Function Tools with Context

```python
@function_tool
def create_todo_tool(ctx: RunContextWrapper[int], title: str, description: Optional[str] = None):
    user_id = ctx.context  # Access user_id from context
    # ... tool implementation
```

#### 3. Agent with Tools

```python
agent = Agent(
    name="Todo Assistant",
    instructions="...",
    model=gemini_model,
    tools=[create_todo_tool, list_todos_tool, ...]
)
```

#### 4. Running the Agent

```python
result = await Runner.run(
    agent,
    last_message,
    context=user_id  # Pass user_id as context
)
```

## 🆚 Comparison: Old vs New

### Old Implementation (agent.py)
- Direct Gemini SDK integration
- Manual function calling handling
- Manual tool execution loop
- Synchronous execution

### New Implementation (agent_openai.py)
- OpenAI Agents SDK framework
- Automatic function calling
- Built-in tool execution
- Async/await support
- Better error handling
- Context management
- Multi-agent support (future)

## 🐛 Troubleshooting

### Error: "GEMINI_API_KEY environment variable is not set"
- Check your `backend/.env` file
- Make sure the key is valid
- Restart the backend server

### Error: "Module 'agents' not found"
```bash
cd backend
pip install openai-agents==0.7.0
```

### Error: "Module 'litellm' not found"
```bash
cd backend
pip install litellm==1.50.0
```

### Chatbot not responding
1. Check backend logs for errors
2. Verify Gemini API key is valid
3. Check database connection
4. Ensure user is authenticated

## 📚 Documentation Links

- **OpenAI Agents SDK**: https://github.com/openai/openai-agents-python
- **LiteLLM**: https://docs.litellm.ai/
- **Google Gemini API**: https://ai.google.dev/docs
- **MCP Protocol**: https://modelcontextprotocol.io/

## 🔄 Switching Back to Old Implementation

If you want to use the old direct Gemini implementation:

1. Edit `backend/routes/chat.py`:
```python
from agent import run_agent  # Instead of agent_openai
```

2. Change the function call:
```python
agent_result = run_agent(  # Instead of await run_agent_openai
    user_id=user_id,
    messages=message_history
)
```

3. Make the endpoint synchronous:
```python
def chat(...):  # Remove async
```

## ✅ Next Steps

- Test all todo operations
- Add more advanced agent features
- Implement multi-agent workflows
- Add conversation memory
- Implement streaming responses
