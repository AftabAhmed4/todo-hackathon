"""
Chat API endpoint for AI-powered todo management.

Stateless endpoint that processes user messages through the AI agent.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from db import get_session
from models import Conversation, Message, MessageRole, User
from agent import run_agent  # Using native Google Generative AI SDK
from auth import get_current_user


router = APIRouter(prefix="/api/chat", tags=["chat"])


# Request/Response Schemas
class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    message: str
    conversation_id: Optional[int] = None


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    response: str
    conversation_id: int
    message_id: int
    tool_calls: Optional[List[Dict[str, Any]]] = None


@router.post("/", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user)
) -> ChatResponse:
    """
    Process a chat message through the AI agent.

    This is a stateless endpoint that:
    1. Loads conversation history from database
    2. Sends context to AI agent
    3. Executes any tool calls
    4. Stores messages in database
    5. Returns agent response

    Args:
        request: ChatRequest with message and optional conversation_id
        session: Database session
        user_id: Authenticated user ID from JWT token

    Returns:
        ChatResponse with agent response and conversation metadata
    """
    try:
        # Verify user exists
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get or create conversation
        if request.conversation_id:
            # Load existing conversation
            conversation = session.exec(
                select(Conversation).where(
                    Conversation.id == request.conversation_id,
                    Conversation.user_id == user_id
                )
            ).first()

            if not conversation:
                raise HTTPException(
                    status_code=404,
                    detail="Conversation not found or you don't have permission to access it"
                )

            # Load conversation history
            messages = session.exec(
                select(Message)
                .where(Message.conversation_id == conversation.id)
                .order_by(Message.created_at)
            ).all()

            # Format messages for agent
            message_history = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

        else:
            # Create new conversation
            conversation = Conversation(
                user_id=user_id,
                title=request.message[:50] + "..." if len(request.message) > 50 else request.message
            )
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

            message_history = []

        # Add user message to history
        message_history.append({
            "role": MessageRole.USER.value,
            "content": request.message
        })

        # Store user message in database
        user_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.USER.value,
            content=request.message
        )
        session.add(user_message)
        session.commit()
        session.refresh(user_message)

        # Run agent with conversation context (native Google Generative AI SDK)
        agent_result = run_agent(
            user_id=user_id,
            messages=message_history
        )

        if not agent_result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=f"Agent error: {agent_result.get('error', 'Unknown error')}"
            )

        # Store assistant message in database
        assistant_message = Message(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT.value,
            content=agent_result["response"]
        )
        session.add(assistant_message)

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)

        session.commit()
        session.refresh(assistant_message)

        return ChatResponse(
            response=agent_result["response"],
            conversation_id=conversation.id,
            message_id=assistant_message.id,
            tool_calls=agent_result.get("tool_calls")
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.get("/conversations", response_model=List[Dict[str, Any]])
def list_conversations(
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    List all conversations for a user.

    Args:
        session: Database session
        user_id: Authenticated user ID from JWT token

    Returns:
        List of conversations with metadata
    """
    try:
        conversations = session.exec(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        ).all()

        return [
            {
                "id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat()
            }
            for conv in conversations
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list conversations: {str(e)}"
        )


@router.get("/conversations/{conversation_id}/messages", response_model=List[Dict[str, Any]])
def get_conversation_messages(
    conversation_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    """
    Get all messages in a conversation.

    Args:
        conversation_id: ID of the conversation
        session: Database session
        user_id: Authenticated user ID from JWT token

    Returns:
        List of messages in chronological order
    """
    try:
        # Verify conversation ownership
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found or you don't have permission to access it"
            )

        # Get messages
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        ).all()

        return [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get conversation messages: {str(e)}"
        )
