"""
app.py — PropScribe AI Entry Point & Router

This is the ONLY file you run: streamlit run app.py

Routing logic:
  1. Not logged in + page == "landing"  →  show landing page
  2. Not logged in + page == "auth"     →  show login/signup page
  3. Logged in                          →  show main PropScribe app

File structure (all files must be in the same folder):
  app.py          ← this file (run this)
  landing.py      ← landing page with video background
  auth_page.py    ← login / signup / Google OAuth
  auth.py         ← auth utilities (register, login, session)
  main_app.py     ← the PropScribe listing generator
  generate.py     ← AI generation logic (from Week 1/2)
  prompts.py      ← prompt templates (from Week 1/2)
  config.py       ← API key loader (from Week 1)
  style.css       ← design system (injected on every page)
  users.json      ← auto-created when first user signs up (add to .gitignore)
  .env            ← your API keys (never commit this)
"""

import streamlit as st

# ── Page config ───────────────────────────────────────────────
# Must be the very first Streamlit call in the entire app
# All page modules import from here — none call set_page_config themselves
st.set_page_config(
    page_title="PropScribe AI — Property Listing Generator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ── Load global CSS ───────────────────────────────────────────
# Injected on every page so fonts, colors, and base styles are always present
def load_css(filepath: str):
    try:
        with open(filepath, "r") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # style.css is missing — app still runs but without custom styles
        st.warning("style.css not found. Make sure it is in the same folder as app.py.")

load_css("style.css")


# ── Session state defaults ────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "auth_tab" not in st.session_state:
    st.session_state.auth_tab = "login"

if "theme" not in st.session_state:
    st.session_state.theme = "dark"


# ── Router ────────────────────────────────────────────────────
# Check if user is authenticated first
user = st.session_state.get("user")

if user:
    # ── Authenticated: show the main PropScribe app ───────────
    from main_app import show_main_app
    show_main_app()

else:
    # ── Not authenticated: landing or auth page ───────────────
    page = st.session_state.get("page", "landing")

    if page == "auth":
        from auth_page import show_auth_page
        show_auth_page()
    else:
        # Default to landing page
        from landing import show_landing
        show_landing()