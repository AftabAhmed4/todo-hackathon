# 🚀 Quick Start Guide - OpenAI Agents SDK + Gemini

## Step 1: Install Dependencies

Open terminal in the `backend` folder:

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Verify Setup

Run the test script:

```bash
python test_agent_setup.py
```

You should see:
```
✅ All tests passed! Your setup is ready.
```

## Step 3: Start the Backend

```bash
python -m uvicorn main:app --reload --port 8000
```

## Step 4: Start the Frontend

Open a new terminal:

```bash
cd frontend
npm run dev
```

## Step 5: Test the Chatbot

1. Open browser: http://localhost:3000
2. Sign up or sign in
3. Go to: http://localhost:3000/chat
4. Try these commands:

```
"Add a todo to buy groceries"
"Show me my todos"
"Mark todo 1 as complete"
"Delete todo 2"
```

## 🎯 What You Built

- **OpenAI Agents SDK** - Professional agent framework
- **Google Gemini** - Via LiteLLM integration
- **MCP Tools** - 5 todo management tools
- **Function Calling** - Automatic tool execution
- **Context Management** - User-specific operations

## 📁 Key Files

```
backend/
├── agent_openai.py          # NEW: OpenAI Agents + Gemini
├── routes/chat.py            # Updated: Async endpoint
├── requirements.txt          # Updated: New dependencies
└── test_agent_setup.py       # NEW: Test script
```

## 🐛 Troubleshooting

### "Module 'agents' not found"
```bash
pip install openai-agents==0.7.0
```

### "Module 'litellm' not found"
```bash
pip install litellm==1.50.0
```

### "GEMINI_API_KEY not set"
Check your `backend/.env` file has:
```
GEMINI_API_KEY=your_key_here
```

## 📚 Documentation

- Full setup guide: `SETUP_OPENAI_AGENTS.md`
- OpenAI Agents SDK: https://github.com/openai/openai-agents-python
- LiteLLM: https://docs.litellm.ai/
