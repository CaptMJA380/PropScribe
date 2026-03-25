"""
auth.py — PropScribe AI Authentication Utilities
Handles: user registration, login, Google OAuth, session management
Users stored locally in users.json (replace with Supabase in Week 4)
"""

import bcrypt
import json
import os
import streamlit as st

USERS_FILE = "users.json"


def load_users() -> dict:
    """Load all users from JSON. Returns empty dict if file does not exist."""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users: dict):
    """Save users dict back to JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def register_user(email: str, name: str, password: str):
    """
    Register a new user with email and password.
    Returns: (success: bool, message: str)
    """
    users = load_users()
    email = email.lower().strip()

    if not email or "@" not in email or "." not in email:
        return False, "Please enter a valid email address."
    if len(name.strip()) < 2:
        return False, "Please enter your full name (at least 2 characters)."
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if email in users:
        return False, "This email is already registered. Please sign in instead."

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    users[email] = {
        "name": name.strip(),
        "email": email,
        "password": hashed,
        "provider": "email",
        "listings_used_total": 0,
        "plan": "free"
    }
    save_users(users)
    return True, "Account created successfully."


def login_user(email: str, password: str):
    """
    Authenticate a user with email and password.
    Returns: (success: bool, user_dict or error_message)
    """
    users = load_users()
    email = email.lower().strip()

    if not email:
        return False, "Please enter your email address."
    if not password:
        return False, "Please enter your password."
    if email not in users:
        return False, "No account found with this email. Please sign up first."

    user = users[email]

    if user.get("provider") == "google":
        return False, "This account uses Google sign-in. Please click Continue with Google."

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        return False, "Incorrect password. Please try again."

    return True, user


def register_or_login_google_user(email: str, name: str) -> dict:
    """
    Called after a successful Google OAuth flow.
    Creates account on first login, or signs in if account already exists.
    """
    users = load_users()
    email = email.lower().strip()

    if email not in users:
        users[email] = {
            "name": name,
            "email": email,
            "password": None,
            "provider": "google",
            "listings_used_total": 0,
            "plan": "free"
        }
        save_users(users)

    return users[email]


def set_session_user(user: dict):
    """Store authenticated user in Streamlit session state."""
    st.session_state.user = user
    st.session_state.listing_count = 0
    st.session_state.last_result = None


def get_session_user() -> dict | None:
    """Get the currently logged-in user, or None."""
    return st.session_state.get("user")


def logout():
    """Clear all session state and return to landing page."""
    for key in ["user", "last_result", "listing_count", "page"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.page = "landing"