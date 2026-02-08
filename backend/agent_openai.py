"""
OpenAI Agents SDK with Gemini API for Todo Management (Fixed Version).

Uses OpenAI Agents SDK with LiteLLM to connect to Google Gemini,
with proper user context handling for MCP tools.
"""
import os
from typing import Dict, Any, List, Optional
from functools import partial
from agents import Agent, Runner, function_tool, RunContextWrapper
from agents.extensions.models.litellm_model import LitellmModel
from sqlmodel import Session, select
from models import Task, TaskStatus
from db import engine
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# MCP Tool Functions with Context Support

@function_tool
def create_todo_tool(ctx: RunContextWrapper[int], title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Create a new todo for the user.

    Args:
        ctx: Run context containing user_id
        title: Title of the todo (required, max 500 characters)
        description: Optional description of the todo

    Returns:
        Dictionary with success status and created todo data
    """
    user_id = ctx.context
    try:
        with Session(engine) as session:
            new_task = Task(
                user_id=user_id,
                title=title,
                description=description,
                status=TaskStatus.PENDING.value
            )

            session.add(new_task)
            session.commit()
            session.refresh(new_task)

            return {
                "success": True,
                "message": f"Todo '{new_task.title}' created successfully",
                "todo": {
                    "id": new_task.id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "status": new_task.status,
                    "created_at": new_task.created_at.isoformat(),
                    "updated_at": new_task.updated_at.isoformat()
                }
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create todo: {str(e)}"
        }


@function_tool
def list_todos_tool(ctx: RunContextWrapper[int], status: Optional[str] = None) -> Dict[str, Any]:
    """List all todos for the user, optionally filtered by status.

    Args:
        ctx: Run context containing user_id
        status: Filter by status (pending, in_progress, completed)

    Returns:
        Dictionary with success status and list of todos
    """
    user_id = ctx.context
    try:
        with Session(engine) as session:
            query = select(Task).where(Task.user_id == user_id)

            if status:
                query = query.where(Task.status == status)

            tasks = session.exec(query).all()

            todos = [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                for task in tasks
            ]

            return {
                "success": True,
                "count": len(todos),
                "todos": todos
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list todos: {str(e)}"
        }


@function_tool
def update_todo_tool(ctx: RunContextWrapper[int], todo_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """Update a todo's title and/or description.

    Args:
        ctx: Run context containing user_id
        todo_id: ID of the todo to update
        title: New title for the todo
        description: New description for the todo

    Returns:
        Dictionary with success status and updated todo data
    """
    user_id = ctx.context
    try:
        with Session(engine) as session:
            task = session.exec(
                select(Task).where(
                    Task.id == todo_id,
                    Task.user_id == user_id
                )
            ).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Todo with ID {todo_id} not found or you don't have permission to update it"
                }

            if title is not None:
                task.title = title
            if description is not None:
                task.description = description

            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "message": f"Todo '{task.title}' updated successfully",
                "todo": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to update todo: {str(e)}"
        }


@function_tool
def delete_todo_tool(ctx: RunContextWrapper[int], todo_id: int) -> Dict[str, Any]:
    """Delete a todo.

    Args:
        ctx: Run context containing user_id
        todo_id: ID of the todo to delete

    Returns:
        Dictionary with success status
    """
    user_id = ctx.context
    try:
        with Session(engine) as session:
            task = session.exec(
                select(Task).where(
                    Task.id == todo_id,
                    Task.user_id == user_id
                )
            ).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Todo with ID {todo_id} not found or you don't have permission to delete it"
                }

            title = task.title
            session.delete(task)
            session.commit()

            return {
                "success": True,
                "message": f"Todo '{title}' deleted successfully"
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to delete todo: {str(e)}"
        }


@function_tool
def complete_todo_tool(ctx: RunContextWrapper[int], todo_id: int, completed: bool) -> Dict[str, Any]:
    """Toggle a todo's completion status.

    Args:
        ctx: Run context containing user_id
        todo_id: ID of the todo to mark as complete/incomplete
        completed: True to mark as completed, False to mark as pending

    Returns:
        Dictionary with success status and updated todo data
    """
    user_id = ctx.context
    try:
        with Session(engine) as session:
            task = session.exec(
                select(Task).where(
                    Task.id == todo_id,
                    Task.user_id == user_id
                )
            ).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Todo with ID {todo_id} not found or you don't have permission to update it"
                }

            task.status = TaskStatus.COMPLETED.value if completed else TaskStatus.PENDING.value
            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)

            status_text = "completed" if completed else "pending"

            return {
                "success": True,
                "message": f"Todo '{task.title}' marked as {status_text}",
                "todo": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to update todo status: {str(e)}"
        }


def get_gemini_agent() -> Agent:
    """
    Create and return an Agent configured with Gemini via LiteLLM.

    Returns:
        Agent instance configured with Gemini model

    Raises:
        ValueError: If GEMINI_API_KEY is not set
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")

    # Create LiteLLM model for Gemini (Google Generative AI API)
    # Explicitly set environment variables to avoid Vertex AI routing
    os.environ["GEMINI_API_KEY"] = api_key

    # Unset Vertex AI environment variables if they exist
    os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
    os.environ.pop("GOOGLE_CLOUD_PROJECT", None)
    os.environ.pop("VERTEXAI_PROJECT", None)
    os.environ.pop("VERTEXAI_LOCATION", None)

    # Use the correct model format for Google AI (not Vertex AI)
    gemini_model = LitellmModel(
        model="gemini/gemini-1.5-flash",
    )

    # Create agent with tools
    agent = Agent(
        name="Todo Assistant",
        instructions="""You are a helpful todo management assistant. Your role is to help users manage their todo list through natural conversation.

You have access to tools to:
- Create new todo items with a title and optional description
- List all todos, optionally filtered by status (pending, in_progress, completed)
- Update a todo's title and/or description
- Delete a todo permanently
- Mark a todo as completed or incomplete

When users ask you to perform actions, use the appropriate tool. Be conversational and friendly in your responses.

Examples:
- "Add a todo to buy groceries" → Use create_todo_tool
- "Show me my todos" → Use list_todos_tool
- "Mark todo 5 as done" → Use complete_todo_tool with completed=True
- "Delete the first todo" → Use delete_todo_tool
- "Change the title of todo 3 to 'Call dentist'" → Use update_todo_tool

Always confirm actions and provide clear feedback about what was done.""",
        model=gemini_model,
        tools=[
            create_todo_tool,
            list_todos_tool,
            update_todo_tool,
            delete_todo_tool,
            complete_todo_tool,
        ],
    )

    return agent


async def run_agent_openai(user_id: int, messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Run the OpenAI Agents SDK agent with Gemini via LiteLLM.

    This is a stateless function that processes a conversation and returns the agent's response.

    Args:
        user_id: ID of the user (for tool execution context)
        messages: List of conversation messages [{"role": "user/assistant", "content": "..."}]

    Returns:
        Dictionary with agent response and any tool calls made
    """
    try:
        # Get agent
        agent = get_gemini_agent()

        # Get the last user message
        last_message = messages[-1]["content"] if messages else ""

        # Run agent with user_id as context
        result = await Runner.run(
            agent,
            last_message,
            context=user_id  # Pass user_id as context for tools
        )

        # Extract tool calls if any
        tool_calls = []
        if hasattr(result, 'tool_calls') and result.tool_calls:
            for tool_call in result.tool_calls:
                tool_calls.append({
                    "tool": tool_call.name if hasattr(tool_call, 'name') else "unknown",
                    "arguments": tool_call.arguments if hasattr(tool_call, 'arguments') else {},
                })

        return {
            "success": True,
            "response": result.final_output,
            "tool_calls": tool_calls
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Agent execution error: {str(e)}",
            "response": "I'm sorry, I encountered an error processing your request. Please try again."
        }
