"""
Temporary script to reset a user's password.

Usage: python reset_password.py
"""
import os
from sqlmodel import Session, select
from dotenv import load_dotenv

from db import engine
from models import User
from auth import hash_password

# Load environment variables
load_dotenv()


def reset_user_password(email: str, new_password: str):
    """
    Reset a user's password.

    Args:
        email: User's email address
        new_password: New password to set
    """
    with Session(engine) as session:
        # Find user by email
        statement = select(User).where(User.email == email.lower())
        user = session.exec(statement).first()

        if not user:
            print(f"❌ User with email '{email}' not found.")
            return False

        # Hash the new password
        new_password_hash = hash_password(new_password)

        # Update user's password
        user.password_hash = new_password_hash
        session.add(user)
        session.commit()

        print(f"✅ Password successfully reset for user: {email}")
        print(f"   New password: {new_password}")
        print(f"\nYou can now sign in with:")
        print(f"   Email: {email}")
        print(f"   Password: {new_password}")

        return True


if __name__ == "__main__":
    print("=" * 60)
    print("Password Reset Tool")
    print("=" * 60)

    # Get user input
    email = input("\nEnter user email: ").strip()
    new_password = input("Enter new password (min 8 chars, uppercase, lowercase, number): ").strip()

    # Validate password
    if len(new_password) < 8:
        print("❌ Password must be at least 8 characters")
        exit(1)

    if not any(c.isupper() for c in new_password):
        print("❌ Password must contain at least one uppercase letter")
        exit(1)

    if not any(c.islower() for c in new_password):
        print("❌ Password must contain at least one lowercase letter")
        exit(1)

    if not any(c.isdigit() for c in new_password):
        print("❌ Password must contain at least one number")
        exit(1)

    # Reset password
    print("\nResetting password...")
    reset_user_password(email, new_password)
    print("\n" + "=" * 60)
