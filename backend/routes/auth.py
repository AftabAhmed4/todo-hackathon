"""
Authentication route handlers.

Provides signup and signin endpoints for user authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime

from db import get_session
from models import User
from schemas import SignupRequest, SigninRequest, AuthResponse, UserPublic
from auth import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user account.

    Creates a new user with email/password credentials, hashes the password,
    and returns a JWT token for authentication.

    Args:
        request: Signup request with email and password
        session: Database session

    Returns:
        AuthResponse: User data and JWT token

    Raises:
        HTTPException: 400 if email already exists or validation fails
        HTTPException: 500 if database error occurs
    """
    # Check if email already exists
    existing_user = session.exec(
        select(User).where(User.email == request.email.lower())
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Validate password requirements (additional validation beyond Pydantic)
    password = request.password
    if not any(c.isupper() for c in password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one uppercase letter"
        )
    if not any(c.islower() for c in password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one lowercase letter"
        )
    if not any(c.isdigit() for c in password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one number"
        )

    try:
        # Hash password
        password_hash = hash_password(password)

        # Create new user
        new_user = User(
            email=request.email.lower(),
            password_hash=password_hash,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Create JWT token
        token_data = {
            "user_id": new_user.id,
            "email": new_user.email
        }
        access_token = create_access_token(token_data)

        # Return response
        return AuthResponse(
            user=UserPublic(
                id=new_user.id,
                email=new_user.email,
                created_at=new_user.created_at
            ),
            token=access_token,
            message="Account created successfully"
        )

    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating your account"
        )


@router.post("/signin", response_model=AuthResponse)
async def signin(
    request: SigninRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate an existing user.

    Verifies email/password credentials and returns a JWT token.
    Uses generic error messages to prevent user enumeration.

    Args:
        request: Signin request with email and password
        session: Database session

    Returns:
        AuthResponse: User data and JWT token

    Raises:
        HTTPException: 401 if credentials are invalid
        HTTPException: 500 if database error occurs
    """
    try:
        # Lookup user by email
        user = session.exec(
            select(User).where(User.email == request.email.lower())
        ).first()

        # Generic error message for security (don't reveal if email exists)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify password
        if not verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Create JWT token
        token_data = {
            "user_id": user.id,
            "email": user.email
        }
        access_token = create_access_token(token_data)

        # Return response
        return AuthResponse(
            user=UserPublic(
                id=user.id,
                email=user.email,
                created_at=user.created_at
            ),
            token=access_token,
            message="Signed in successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication"
        )
