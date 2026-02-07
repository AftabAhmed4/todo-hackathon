"""
Task CRUD API endpoints.

Provides REST API endpoints for managing user tasks with proper authentication
and authorization.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from typing import List
from datetime import datetime

from db import get_session
from auth import get_current_user
from models import Task, TaskStatus
from schemas import TaskCreate, TaskUpdate, TaskRead, TaskListResponse

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: int,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user)
):
    """
    Create a new task for the authenticated user.

    Args:
        user_id: User ID from path parameter
        task_data: Task creation data (title, description, status)
        session: Database session
        current_user_id: Authenticated user ID from JWT token

    Returns:
        TaskRead: Created task with all fields

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
        HTTPException 400: If validation fails
    """
    # Verify user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create tasks for this user"
        )

    # Validate title
    if not task_data.title or len(task_data.title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required and cannot be empty"
        )

    if len(task_data.title) > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title cannot exceed 500 characters"
        )

    # Validate description if provided
    if task_data.description and len(task_data.description) > 2000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description cannot exceed 2000 characters"
        )

    # Create new task
    new_task = Task(
        user_id=user_id,
        title=task_data.title.strip(),
        description=task_data.description.strip() if task_data.description else None,
        status=task_data.status.value if task_data.status else TaskStatus.PENDING.value,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Save to database
    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    user_id: int,
    page: int = 1,
    page_size: int = 20,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user)
):
    """
    Get paginated list of tasks for the authenticated user.

    Args:
        user_id: User ID from path parameter
        page: Page number (default: 1)
        page_size: Items per page (default: 20, max: 100)
        session: Database session
        current_user_id: Authenticated user ID from JWT token

    Returns:
        TaskListResponse: Paginated list of tasks

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
        HTTPException 400: If pagination parameters are invalid
    """
    # Verify user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view tasks for this user"
        )

    # Validate pagination parameters
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page number must be >= 1"
        )

    if page_size < 1 or page_size > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be between 1 and 100"
        )

    # Calculate offset
    offset = (page - 1) * page_size

    # Query tasks with pagination
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    tasks = session.exec(statement).all()

    # Count total tasks
    count_statement = select(func.count(Task.id)).where(Task.user_id == user_id)
    total = session.exec(count_statement).one()

    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size

    return TaskListResponse(
        items=tasks,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    user_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user)
):
    """
    Get a single task by ID.

    Args:
        user_id: User ID from path parameter
        task_id: Task ID from path parameter
        session: Database session
        current_user_id: Authenticated user ID from JWT token

    Returns:
        TaskRead: Task details

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
        HTTPException 404: If task not found or doesn't belong to user
    """
    # Verify user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view tasks for this user"
        )

    # Query task by ID and user_id
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you do not have permission to access it"
        )

    return task


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    user_id: int,
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user)
):
    """
    Update an existing task.

    Args:
        user_id: User ID from path parameter
        task_id: Task ID from path parameter
        task_data: Task update data (partial update supported)
        session: Database session
        current_user_id: Authenticated user ID from JWT token

    Returns:
        TaskRead: Updated task

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
        HTTPException 404: If task not found or doesn't belong to user
        HTTPException 400: If validation fails
    """
    # Verify user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update tasks for this user"
        )

    # Query task by ID and user_id
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you do not have permission to access it"
        )

    # Validate and update fields
    if task_data.title is not None:
        if not task_data.title or len(task_data.title.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title is required and cannot be empty"
            )
        if len(task_data.title) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot exceed 500 characters"
            )
        task.title = task_data.title.strip()

    if task_data.description is not None:
        if len(task_data.description) > 2000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description cannot exceed 2000 characters"
            )
        task.description = task_data.description.strip() if task_data.description else None

    if task_data.status is not None:
        task.status = task_data.status.value

    # Update timestamp
    task.updated_at = datetime.utcnow()

    # Save changes
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{task_id}")
async def delete_task(
    user_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user)
):
    """
    Delete a task.

    Args:
        user_id: User ID from path parameter
        task_id: Task ID from path parameter
        session: Database session
        current_user_id: Authenticated user ID from JWT token

    Returns:
        dict: Success message with deleted task ID

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
        HTTPException 404: If task not found or doesn't belong to user
    """
    # Verify user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete tasks for this user"
        )

    # Query task by ID and user_id
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you do not have permission to access it"
        )

    # Delete task
    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully", "id": task_id}
