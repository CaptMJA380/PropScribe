"""
auth_page.py — PropScribe AI Authentication Page v2.1
Complete inline form CSS overrides for dark AND light mode.
"""

import os
import streamlit as st
from auth import register_user, login_user, load_users, \
                 register_or_login_google_user, set_session_user


def show_auth_page():
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

    is_dark = st.session_state.theme == "dark"

    bg       = "#080810"     if is_dark else "#F5F2EC"
    card_bg  = "rgba(15,15,26,0.97)" if is_dark else "rgba(255,255,255,0.98)"
    border   = "rgba(255,255,255,0.08)" if is_dark else "rgba(0,0,0,0.1)"
    border_l = "rgba(255,255,255,0.12)" if is_dark else "rgba(0,0,0,0.15)"
    gold     = "#C9A348"     if is_dark else "#9F7625"
    gold_lt  = "#E8C56A"     if is_dark else "#B8892E"
    gold_glow = "rgba(201,163,72,0.12)" if is_dark else "rgba(159,118,37,0.09)"
    text_p   = "#F2EDE0"     if is_dark else "#1A1A2E"
    text_s   = "#9A9AAE"     if is_dark else "#4A4A68"
    text_m   = "#4A4A60"     if is_dark else "#8A8A9E"
    elevated = "#161625"     if is_dark else "#EDEAE2"
    icon_bg  = "rgba(201,163,72,0.1)" if is_dark else "rgba(159,118,37,0.08)"
    succ     = "#3ECF8E"
    orb1 = "rgba(201,163,72,0.07)" if is_dark else "rgba(159,118,37,0.05)"
    orb2 = "rgba(80,80,180,0.05)" if is_dark else "rgba(80,80,180,0.03)"
    overlay_shadow = "0 24px 64px rgba(0,0,0,0.6)" if is_dark else "0 12px 40px rgba(0,0,0,0.1)"
    ele_border = border

    # ── All page CSS injected as raw values ───────────────────
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,400&family=Inter:wght@300;400;500;600;700&display=swap');
    @keyframes floatOrb {{
      0%,100% {{ transform: translate(0,0) scale(1); }}
      33%      {{ transform: translate(28px,-24px) scale(1.06); }}
      66%      {{ transform: translate(-14px,14px) scale(0.96); }}
    }}
    @keyframes fadeUp {{
      from {{ opacity:0; transform:translateY(18px); }}
      to   {{ opacity:1; transform:translateY(0); }}
    }}

    /* Page base */
    body, .stApp {{ background: {bg} !important; color: {text_p} !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    .main .block-container {{ padding: 1.5rem 1rem !important; max-width: 100% !important; }}
    [data-testid="stVerticalBlock"] {{ gap: 0 !important; }}

    /* All Streamlit inputs — dark or light */
    .stTextInput > label, .stSelectbox > label,
    .stMultiSelect > label, .stFileUploader > label {{
      color: {text_s} !important; font-size: 11px !important;
      font-weight: 600 !important; text-transform: uppercase !important;
      letter-spacing: 0.1em !important;
    }}
    .stTextInput > div > div > input {{
      background: {elevated} !important;
      border: 1px solid {border} !important;
      border-radius: 10px !important;
      color: {text_p} !important;
      font-family: 'Inter', sans-serif !important;
      font-size: 14px !important;
    }}
    .stTextInput > div > div > input:focus {{
      border-color: {gold} !important;
      box-shadow: 0 0 0 3px {gold_glow} !important;
    }}
    .stTextInput > div > div > input::placeholder {{ color: {text_m} !important; }}

    /* Password eye icon */
    .stTextInput [data-testid="textInputRootElement"] > div > button {{
      color: {text_m} !important; background: transparent !important; border: none !important;
    }}

    /* Form submit button */
    .stForm [data-testid="baseButton-primary"],
    .stButton > button[kind="primary"] {{
      background: linear-gradient(135deg, {gold}, {gold_lt}) !important;
      color: #080810 !important; border: none !important;
      border-radius: 10px !important; font-family: 'Inter', sans-serif !important;
      font-size: 13px !important; font-weight: 700 !important;
      letter-spacing: 0.06em !important; text-transform: uppercase !important;
      padding: 0.75rem 1.5rem !important;
      box-shadow: 0 4px 20px {gold}40 !important; transition: all 0.22s !important;
    }}
    .stForm [data-testid="baseButton-primary"]:hover,
    .stButton > button[kind="primary"]:hover {{
      transform: translateY(-2px) !important; box-shadow: 0 8px 28px {gold}55 !important;
    }}
    .stButton > button[kind="secondary"] {{
      background: transparent !important; color: {text_s} !important;
      border: 1px solid {border_l} !important; border-radius: 10px !important;
      font-family: 'Inter', sans-serif !important; font-size: 13px !important;
      font-weight: 500 !important; transition: all 0.22s !important;
    }}
    .stButton > button[kind="secondary"]:hover {{
      border-color: {gold} !important; color: {gold} !important;
    }}

    /* Markdown text */
    .stMarkdown p {{ color: {text_s} !important; }}
    </style>
    """, unsafe_allow_html=True)

    # ── Background orbs ───────────────────────────────────────
    st.markdown(f"""
    <div style="position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden;background:{bg}">
      <div style="position:absolute;top:-18%;right:-12%;width:520px;height:520px;border-radius:50%;
                  background:radial-gradient(circle,{orb1} 0%,transparent 70%);
                  animation:floatOrb 9s ease-in-out infinite"></div>
      <div style="position:absolute;bottom:-18%;left:-10%;width:460px;height:460px;border-radius:50%;
                  background:radial-gradient(circle,{orb2} 0%,transparent 70%);
                  animation:floatOrb 12s ease-in-out infinite reverse"></div>
      <div style="position:absolute;top:45%;left:38%;width:280px;height:280px;border-radius:50%;
                  background:radial-gradient(circle,{orb1} 0%,transparent 65%);
                  animation:floatOrb 15s ease-in-out 2s infinite"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Logo ──────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center;margin:2rem 0 1.5rem;position:relative;z-index:1;
                animation:fadeUp .7s ease both">
      <div style="font-family:'Cormorant Garamond',Georgia,serif;font-size:2.1rem;
                  font-weight:600;color:{text_p};letter-spacing:-.01em;margin-bottom:6px">
        PropScribe<span style="color:{gold}"> AI</span>
      </div>
      <div style="font-size:11px;color:{text_m};letter-spacing:.13em;text-transform:uppercase">
        Property Listing Generator
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Center layout ─────────────────────────────────────────
    _, center_col, _ = st.columns([1, 1.6, 1])

    with center_col:
        # Auth card background
        st.markdown(f"""
        <div style="position:relative;z-index:1;
                    background:{card_bg};border:1px solid {border_l};
                    border-radius:22px;padding:2.5rem 2.25rem 2.25rem;
                    box-shadow:{overlay_shadow};
                    backdrop-filter:blur(28px);-webkit-backdrop-filter:blur(28px);
                    animation:fadeUp .55s ease .15s both;overflow:hidden">
          <div style="position:absolute;top:0;left:8%;right:8%;height:1px;
                      background:linear-gradient(90deg,transparent,{gold}70,transparent)"></div>
        </div>
        """, unsafe_allow_html=True)

        # Tab switcher
        default_tab = st.session_state.get("auth_tab", "login")
        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            login_clicked = st.button("Sign In", key="tab_login", use_container_width=True,
                type="primary" if default_tab == "login" else "secondary")
        with tab_col2:
            signup_clicked = st.button("Create Account", key="tab_signup", use_container_width=True,
                type="primary" if default_tab == "signup" else "secondary")

        if login_clicked:
            st.session_state.auth_tab = "login"; st.rerun()
        if signup_clicked:
            st.session_state.auth_tab = "signup"; st.rerun()

        current_tab = st.session_state.get("auth_tab", "login")
        st.markdown("<div style='height:.75rem'></div>", unsafe_allow_html=True)

        # ── Sign In ───────────────────────────────────────────
        if current_tab == "login":
            st.markdown(f"""
            <div style="margin-bottom:1.25rem">
              <div style="font-family:'Cormorant Garamond',serif;font-size:1.55rem;
                          font-weight:600;color:{text_p};margin-bottom:.3rem">Welcome back</div>
              <div style="font-size:13px;color:{text_s}">Sign in to your PropScribe account</div>
            </div>
            """, unsafe_allow_html=True)
            with st.form("login_form", clear_on_submit=False):
                email    = st.text_input("Email address", placeholder="you@example.com", key="login_email")
                password = st.text_input("Password", type="password", placeholder="Your password", key="login_password")
                st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Sign In →", type="primary", use_container_width=True)
                if submitted:
                    success, result = login_user(email, password)
                    if success:
                        set_session_user(result); st.session_state.page = "app"; st.rerun()
                    else:
                        st.markdown(f"""
                        <div style="background:rgba(248,113,113,0.1);border:1px solid rgba(248,113,113,0.25);
                                    border-radius:8px;padding:10px 14px;font-size:13px;color:#F87171;
                                    margin-top:8px">⚠️ {result}</div>
                        """, unsafe_allow_html=True)

        # ── Create Account ────────────────────────────────────
        else:
            st.markdown(f"""
            <div style="margin-bottom:1.25rem">
              <div style="font-family:'Cormorant Garamond',serif;font-size:1.55rem;
                          font-weight:600;color:{text_p};margin-bottom:.3rem">Create account</div>
              <div style="font-size:13px;color:{text_s}">3 free listings to start — no credit card needed</div>
            </div>
            """, unsafe_allow_html=True)
            with st.form("signup_form", clear_on_submit=False):
                name     = st.text_input("Full name", placeholder="Rahul Sharma", key="signup_name")
                email    = st.text_input("Email address", placeholder="you@example.com", key="signup_email")
                password = st.text_input("Password", type="password", placeholder="At least 8 characters", key="signup_password")
                st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("Create Account →", type="primary", use_container_width=True)
                if submitted:
                    success, message = register_user(email, name, password)
                    if success:
                        users = load_users(); user = users.get(email.lower().strip())
                        if user:
                            set_session_user(user); st.session_state.page = "app"; st.rerun()
                    else:
                        st.markdown(f"""
                        <div style="background:rgba(248,113,113,0.1);border:1px solid rgba(248,113,113,0.25);
                                    border-radius:8px;padding:10px 14px;font-size:13px;color:#F87171;
                                    margin-top:8px">⚠️ {message}</div>
                        """, unsafe_allow_html=True)

        # ── OR divider ────────────────────────────────────────
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;margin:1.25rem 0;
                    color:{text_m};font-size:11px;letter-spacing:.08em;text-transform:uppercase">
          <div style="flex:1;height:1px;background:{border}"></div>or continue with
          <div style="flex:1;height:1px;background:{border}"></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Google OAuth ──────────────────────────────────────
        google_client_id     = os.getenv("GOOGLE_CLIENT_ID")
        google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

        if google_client_id and google_client_secret:
            try:
                from streamlit_oauth import OAuth2Component
                import jwt
                redirect_uri = os.getenv("REDIRECT_URI", "http://localhost:8501")
                oauth2 = OAuth2Component(
                    client_id=google_client_id, client_secret=google_client_secret,
                    authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
                    token_endpoint="https://oauth2.googleapis.com/token",
                    refresh_token_endpoint="https://oauth2.googleapis.com/token",
                    revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
                )
                result = oauth2.authorize_button("Continue with Google",
                    icon="https://www.google.com/favicon.ico",
                    redirect_uri=redirect_uri, scope="openid email profile",
                    key="google_oauth", use_container_width=True)
                if result and "token" in result:
                    id_token     = result["token"].get("id_token", "")
                    payload      = jwt.decode(id_token, options={"verify_signature": False})
                    google_email = payload.get("email", "")
                    google_name  = payload.get("name", "Google User")
                    if google_email:
                        user = register_or_login_google_user(google_email, google_name)
                        set_session_user(user); st.session_state.page = "app"; st.rerun()
            except ImportError:
                st.markdown(f'<div style="font-size:12px;color:{text_m};text-align:center;padding:8px">Run: pip install streamlit-oauth PyJWT to enable Google login</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:center;gap:10px;
                        padding:11px 16px;background:{elevated};border:1px solid {border};
                        border-radius:10px;cursor:default;user-select:none">
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z" fill="#4285F4"/>
                <path d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 009 18z" fill="#34A853"/>
                <path d="M3.964 10.71A5.41 5.41 0 013.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 000 9c0 1.452.348 2.827.957 4.042l3.007-2.332z" fill="#FBBC05"/>
                <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 00.957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z" fill="#EA4335"/>
              </svg>
              <span style="font-size:14px;font-weight:500;color:{text_m}">Continue with Google</span>
            </div>
            <div style="font-size:11px;color:{text_m};text-align:center;margin-top:7px;line-height:1.5">
              Add GOOGLE_CLIENT_ID &amp; GOOGLE_CLIENT_SECRET to .env to enable
            </div>
            """, unsafe_allow_html=True)

        # ── Bottom actions ────────────────────────────────────
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        bot1, bot2 = st.columns(2)
        with bot1:
            if st.button("← Back to home", key="back_home", type="secondary", use_container_width=True):
                st.session_state.page = "landing"; st.rerun()
        with bot2:
            tgl = "☀️ Light mode" if is_dark else "🌙 Dark mode"
            if st.button(tgl, key="theme_toggle_auth", use_container_width=True):
                st.session_state.theme = "light" if is_dark else "dark"; st.rerun()

        st.markdown(f"""
        <div style="text-align:center;margin-top:.75rem;font-size:11px;color:{text_m};line-height:1.65">
          By signing up you agree to our Terms of Service.<br>Your data is never sold or shared.
        </div>
        """, unsafe_allow_html=True)

    # Feature teasers
    feats = ["3 free listings", "English, Hindi &amp; Marathi", "99acres &amp; MagicBricks ready", "WhatsApp &amp; Email templates"]
    st.markdown(f"""
    <div style="display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;margin-top:2rem;padding:0 8%">
      {"".join([f'<span style="display:flex;align-items:center;gap:6px;font-size:12px;color:{text_m}"><span style="color:{succ}">✓</span>{f}</span>' for f in feats])}
    </div>
    """, unsafe_allow_html=True)