# Quick Start Guide - Todo AI Chatbot

## Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL database (Neon)
- OpenAI API key

## 🚀 Quick Setup (5 minutes)

### Step 1: Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit .env file and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here

# Start the server
uvicorn main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 2: Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

**Expected output:**
```
▲ Next.js 16.0.0
- Local:        http://localhost:3000
```

### Step 3: Test the System

1. **Create an account:**
   - Open http://localhost:3000/signup
   - Enter email and password
   - Click "Sign Up"

2. **Access the chat:**
   - Navigate to http://localhost:3000/chat
   - You should see the chat interface

3. **Try these commands:**
   ```
   "Add a todo to buy groceries"
   "Show me my todos"
   "Mark todo 1 as complete"
   "Delete todo 1"
   ```

## 🔧 Configuration

### Required Environment Variables

**Backend (.env):**
```env
DATABASE_URL=postgresql://...  # Already configured
BETTER_AUTH_SECRET=...         # Already configured
OPENAI_API_KEY=sk-...          # ⚠️ YOU MUST ADD THIS
FRONTEND_URL=http://localhost:3000
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## ✅ Verification Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can create an account at /signup
- [ ] Can sign in at /signin
- [ ] Can access /chat when authenticated
- [ ] Chat responds to messages
- [ ] Todos are created via chat commands

## 🐛 Troubleshooting

### "OpenAI API key not set"
**Solution:** Add `OPENAI_API_KEY=sk-your-key-here` to `backend/.env`

### "Database connection failed"
**Solution:** Check `DATABASE_URL` in `backend/.env` is valid

### "Cannot connect to backend"
**Solution:** Ensure backend is running on port 8000

### "Session expired" error
**Solution:** Sign in again at /signin

## 📝 Example Conversation

```
You: Add a todo to buy groceries
AI: Todo 'buy groceries' created successfully

You: Show me my todos
AI: You have 1 todo:
    1. buy groceries (pending)

You: Mark todo 1 as complete
AI: Todo 'buy groceries' marked as completed

You: List completed todos
AI: You have 1 completed todo:
    1. buy groceries (completed)
```

## 🎯 What You Can Do

### Create Todos
- "Add a todo to [task]"
- "Create a task to [task]"
- "Remind me to [task]"

### List Todos
- "Show me my todos"
- "List all tasks"
- "What are my pending todos?"
- "Show completed tasks"

### Update Todos
- "Update todo [id] to [new text]"
- "Change todo [id] title to [new title]"

### Complete Todos
- "Mark todo [id] as complete"
- "Complete task [id]"
- "Mark todo [id] as incomplete"

### Delete Todos
- "Delete todo [id]"
- "Remove task [id]"

## 🔐 Security Notes

- Passwords are hashed with bcrypt
- JWT tokens expire after 24 hours
- All API endpoints are authenticated
- User data is isolated by user_id

## 📚 Additional Resources

- Full documentation: `IMPLEMENTATION.md`
- API documentation: http://localhost:8000/docs (when backend is running)
- Project structure: See `IMPLEMENTATION.md`

## 🆘 Need Help?

1. Check the logs in your terminal
2. Review `IMPLEMENTATION.md` for detailed information
3. Verify all environment variables are set
4. Ensure all dependencies are installed

## 🎉 You're Ready!

Your Todo AI Chatbot is now running. Start chatting at http://localhost:3000/chat
