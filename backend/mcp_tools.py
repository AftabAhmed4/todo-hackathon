"""
MCP Tools for Todo Management.

Stateless tools that interact with the database to perform CRUD operations on todos.
Each tool is designed to be called by the AI agent with structured inputs.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from models import Task, TaskStatus
from db import engine
from datetime import datetime


# Tool Input/Output Schemas
class CreateTodoInput(BaseModel):
    """Input schema for creating a new todo."""
    user_id: int = Field(description="ID of the user creating the todo")
    title: str = Field(description="Title of the todo (required, max 500 characters)")
    description: Optional[str] = Field(default=None, description="Optional description of the todo")


class TodoOutput(BaseModel):
    """Output schema for a single todo."""
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: str
    updated_at: str


class ListTodosInput(BaseModel):
    """Input schema for listing todos."""
    user_id: int = Field(description="ID of the user whose todos to list")
    status: Optional[str] = Field(default=None, description="Filter by status (pending, in_progress, completed)")


class UpdateTodoInput(BaseModel):
    """Input schema for updating a todo."""
    user_id: int = Field(description="ID of the user who owns the todo")
    todo_id: int = Field(description="ID of the todo to update")
    title: Optional[str] = Field(default=None, description="New title for the todo")
    description: Optional[str] = Field(default=None, description="New description for the todo")


class DeleteTodoInput(BaseModel):
    """Input schema for deleting a todo."""
    user_id: int = Field(description="ID of the user who owns the todo")
    todo_id: int = Field(description="ID of the todo to delete")


class CompleteTodoInput(BaseModel):
    """Input schema for toggling todo completion."""
    user_id: int = Field(description="ID of the user who owns the todo")
    todo_id: int = Field(description="ID of the todo to mark as complete/incomplete")
    completed: bool = Field(description="True to mark as completed, False to mark as pending")


# MCP Tool Functions
def create_todo(input_data: CreateTodoInput) -> Dict[str, Any]:
    """
    Create a new todo for the user.

    Args:
        input_data: CreateTodoInput with user_id, title, and optional description

    Returns:
        Dictionary with success status and created todo data
    """
    try:
        with Session(engine) as session:
            # Create new task
            new_task = Task(
                user_id=input_data.user_id,
                title=input_data.title,
                description=input_data.description,
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


def list_todos(input_data: ListTodosInput) -> Dict[str, Any]:
    """
    List all todos for the user, optionally filtered by status.

    Args:
        input_data: ListTodosInput with user_id and optional status filter

    Returns:
        Dictionary with success status and list of todos
    """
    try:
        with Session(engine) as session:
            # Build query
            query = select(Task).where(Task.user_id == input_data.user_id)

            # Apply status filter if provided
            if input_data.status:
                query = query.where(Task.status == input_data.status)

            # Execute query
            tasks = session.exec(query).all()

            # Format todos
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


def update_todo(input_data: UpdateTodoInput) -> Dict[str, Any]:
    """
    Update a todo's title and/or description.

    Args:
        input_data: UpdateTodoInput with user_id, todo_id, and fields to update

    Returns:
        Dictionary with success status and updated todo data
    """
    try:
        with Session(engine) as session:
            # Find the task
            task = session.exec(
                select(Task).where(
                    Task.id == input_data.todo_id,
                    Task.user_id == input_data.user_id
                )
            ).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Todo with ID {input_data.todo_id} not found or you don't have permission to update it"
                }

            # Update fields
            if input_data.title is not None:
                task.title = input_data.title
            if input_data.description is not None:
                task.description = input_data.description

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


def delete_todo(input_data: DeleteTodoInput) -> Dict[str, Any]:
    """
    Delete a todo.

    Args:
        input_data: DeleteTodoInput with user_id and todo_id

    Returns:
        Dictionary with success status
    """
    try:
        with Session(engine) as session:
            # Find the task
            task = session.exec(
                select(Task).where(
                    Task.id == input_data.todo_id,
                    Task.user_id == input_data.user_id
                )
            ).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Todo with ID {input_data.todo_id} not found or you don't have permission to delete it"
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


def complete_todo(input_data: CompleteTodoInput) -> Dict[str, Any]:
    """
    Toggle a todo's completion status.

    Args:
        input_data: CompleteTodoInput with user_id, todo_id, and completed status

    Returns:
        Dictionary with success status and updated todo data
    """
    try:
        with Session(engine) as session:
            # Find the task
            task = session.exec(
                select(Task).where(
                    Task.id == input_data.todo_id,
                    Task.user_id == input_data.user_id
                )
            ).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Todo with ID {input_data.todo_id} not found or you don't have permission to update it"
                }

            # Update status
            task.status = TaskStatus.COMPLETED.value if input_data.completed else TaskStatus.PENDING.value
            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)

            status_text = "completed" if input_data.completed else "pending"

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


# Tool Registry for AI Agent
TOOLS = {
    "create_todo": {
        "function": create_todo,
        "input_schema": CreateTodoInput,
        "description": "Create a new todo item for the user with a title and optional description"
    },
    "list_todos": {
        "function": list_todos,
        "input_schema": ListTodosInput,
        "description": "List all todos for the user, optionally filtered by status (pending, in_progress, completed)"
    },
    "update_todo": {
        "function": update_todo,
        "input_schema": UpdateTodoInput,
        "description": "Update a todo's title and/or description"
    },
    "delete_todo": {
        "function": delete_todo,
        "input_schema": DeleteTodoInput,
        "description": "Delete a todo permanently"
    },
    "complete_todo": {
        "function": complete_todo,
        "input_schema": CompleteTodoInput,
        "description": "Mark a todo as completed or incomplete"
    }
}
