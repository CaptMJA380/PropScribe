"""
landing.py — PropScribe AI Landing Page v2.1
- Video: uses full http://localhost:8501/app/static/ URL (works in iframe)
- CTA buttons: inside hero HTML (perfect alignment, no Streamlit columns)
- Light mode: all colors injected as raw values (no CSS vars Streamlit can override)
"""

import os
import streamlit as st
import streamlit.components.v1 as components
import textwrap


def md(html: str):
    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)


def asset_exists(filename: str) -> bool:
    return os.path.isfile(os.path.join(".streamlit", "static", filename))


def get_streamlit_input_css(bg, border, text_p, text_m, gold, gold_glow, elevated, card_bg, text_s):
    """Returns strong CSS overrides for all Streamlit form elements."""
    return f"""
    /* ── Streamlit form overrides (raw values, no vars) ── */
    .stTextInput > label, .stSelectbox > label,
    .stMultiSelect > label, .stFileUploader > label {{
      color: {text_s} !important; font-size: 11px !important;
      font-weight: 600 !important; text-transform: uppercase !important;
      letter-spacing: 0.1em !important;
    }}
    .stTextInput > div > div > input {{
      background: {elevated} !important; border: 1px solid {border} !important;
      border-radius: 10px !important; color: {text_p} !important;
      font-family: 'Inter', sans-serif !important; font-size: 14px !important;
      padding: 0.65rem 0.9rem !important;
    }}
    .stTextInput > div > div > input:focus {{
      border-color: {gold} !important; box-shadow: 0 0 0 3px {gold_glow} !important;
    }}
    .stTextInput > div > div > input::placeholder {{ color: {text_m} !important; }}
    .stSelectbox > div > div {{
      background: {elevated} !important; border: 1px solid {border} !important;
      border-radius: 10px !important; color: {text_p} !important;
    }}
    .stSelectbox > div > div > div {{ color: {text_p} !important; }}
    .stSelectbox > div > div:hover {{ border-color: {gold}55 !important; }}
    [data-baseweb="popover"] {{
      background: {elevated} !important; border: 1px solid {border} !important;
      border-radius: 10px !important;
    }}
    [data-baseweb="menu"] {{ background: {elevated} !important; }}
    [role="option"] {{ background: transparent !important; color: {text_s} !important; }}
    [role="option"]:hover, [aria-selected="true"] {{
      background: {gold_glow} !important; color: {gold} !important;
    }}
    .stMultiSelect > div > div {{
      background: {elevated} !important; border: 1px solid {border} !important;
      border-radius: 10px !important;
    }}
    [data-baseweb="tag"] {{
      background: {gold_glow} !important; border-radius: 5px !important;
      color: {gold} !important; font-size: 12px !important;
    }}
    [data-testid="stFileUploader"] > div {{
      background: {elevated} !important; border: 1px dashed {gold}40 !important;
      border-radius: 14px !important; padding: 1.2rem !important;
    }}
    .stTextArea > label {{ display: none !important; }}
    .stTextArea > div > div > textarea {{
      background: {elevated} !important; border: 1px solid {border} !important;
      border-radius: 10px !important; color: {text_p} !important;
      font-family: 'Inter', sans-serif !important; font-size: 13.5px !important;
      line-height: 1.7 !important; padding: 1rem !important;
    }}
    .stTextArea > div > div > textarea:focus {{
      border-color: {gold} !important; box-shadow: 0 0 0 3px {gold_glow} !important;
    }}
    .stMarkdown p {{ color: {text_s} !important; line-height: 1.7 !important; }}
    [data-testid="stSidebar"] .stMarkdown p {{ color: {text_s} !important; font-size: 13px !important; }}
    [data-testid="stSidebar"] hr {{ border-color: {border} !important; margin: 1rem 0 !important; }}
    .stTabs [data-baseweb="tab-list"] {{
      background: {elevated} !important; border-radius: 10px !important; padding: 4px !important;
    }}
    .stTabs [data-baseweb="tab"] {{
      background: transparent !important; color: {text_m} !important;
      border-radius: 7px !important;
    }}
    .stTabs [aria-selected="true"] {{
      background: {card_bg} !important; color: {gold} !important;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    }}
    hr {{ border-top: 1px solid {border} !important; }}
    .stSpinner > div > div {{ border-color: {gold} transparent transparent transparent !important; }}
    .stButton > button[kind="primary"] {{
      background: linear-gradient(135deg, {gold}, {gold}CC) !important;
      color: #080810 !important; border: none !important;
      border-radius: 10px !important; font-weight: 600 !important;
      font-size: 13px !important; letter-spacing: 0.06em !important;
      text-transform: uppercase !important; padding: 0.75rem 1.5rem !important;
      box-shadow: 0 4px 20px {gold}40 !important; transition: all 0.22s !important;
    }}
    .stButton > button[kind="primary"]:hover {{
      transform: translateY(-2px) !important; box-shadow: 0 8px 30px {gold}55 !important;
    }}
    .stButton > button[kind="secondary"] {{
      background: transparent !important; color: {text_s} !important;
      border: 1px solid {border} !important; border-radius: 10px !important;
      font-size: 13px !important; font-weight: 500 !important;
      padding: 0.65rem 1.25rem !important; transition: all 0.22s !important;
    }}
    .stButton > button[kind="secondary"]:hover {{
      border-color: {gold} !important; color: {gold} !important;
    }}
    """


def show_landing():

    # ── Theme state ───────────────────────────────────────────
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

    theme = st.session_state.theme
    is_dark = theme == "dark"

    # ── All theme colors as raw values ────────────────────────
    bg       = "#080810" if is_dark else "#F5F2EC"
    surface  = "#0F0F1A" if is_dark else "#FFFFFF"
    elevated = "#161625" if is_dark else "#EDEAE2"
    card_bg  = "rgba(22,22,37,0.95)" if is_dark else "rgba(255,255,255,0.97)"
    border   = "rgba(255,255,255,0.07)" if is_dark else "rgba(0,0,0,0.1)"
    gold     = "#C9A348" if is_dark else "#9F7625"
    gold_lt  = "#E8C56A" if is_dark else "#B8892E"
    gold_glow = "rgba(201,163,72,0.1)" if is_dark else "rgba(159,118,37,0.08)"
    text_p   = "#F2EDE0" if is_dark else "#1A1A2E"
    text_s   = "#9A9AAE" if is_dark else "#4A4A68"
    text_m   = "#4A4A60" if is_dark else "#8A8A9E"
    icon_bg  = "rgba(201,163,72,0.12)" if is_dark else "rgba(159,118,37,0.1)"
    feat_bg  = "rgba(22,22,37,0.92)" if is_dark else "rgba(255,255,255,0.96)"
    section_bg = "#0A0A14" if is_dark else "#EDEAE2"
    orb1 = "rgba(201,163,72,0.09)" if is_dark else "rgba(159,118,37,0.06)"
    orb2 = "rgba(80,80,200,0.05)" if is_dark else "rgba(80,80,200,0.03)"
    overlay_rgb = "8,8,16" if is_dark else "245,242,236"
    nav_blur_bg = "rgba(8,8,16,0.7)" if is_dark else "rgba(245,242,236,0.8)"
    succ = "#3ECF8E"
    # Video / image paths — full URL so iframe can resolve them
    VIDEO_URL  = "http://localhost:8501/app/static/bg_video.mp4"
    VIDEO_URL2 = "http://localhost:8501/app/static/bg_video_2.mp4"
    IMAGE_URL  = "http://localhost:8501/app/static/bg_image.jpg"

    has_video  = asset_exists("bg_video.mp4")
    has_video2 = asset_exists("bg_video_2.mp4")
    has_image  = asset_exists("bg_image.jpg")

    # ── Page base styles ──────────────────────────────────────
    st.markdown(f"""
    <style>
    body, .stApp {{ background: {bg} !important; color: {text_p} !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    .main .block-container {{ padding: 0 !important; max-width: 100% !important; }}
    [data-testid="stVerticalBlock"] {{ gap: 0 !important; }}
    ::-webkit-scrollbar {{ width: 4px; }}
    ::-webkit-scrollbar-thumb {{ background: {elevated}; border-radius: 2px; }}
    /* Feature cards */
    .feat-card {{
      border: 1px solid {border}; border-radius: 16px; padding: 1.85rem;
      background: {feat_bg}; backdrop-filter: blur(14px);
      transition: border-color 0.28s, transform 0.28s, box-shadow 0.28s;
    }}
    .feat-card:hover {{
      border-color: {gold}55; transform: translateY(-6px);
      box-shadow: 0 20px 50px rgba(0,0,0,0.25), 0 0 30px {gold}18;
    }}
    .process-card {{
      border: 1px solid {border}; border-radius: 16px; padding: 1.75rem;
      background: {feat_bg}; transition: all 0.28s; position: relative; overflow: hidden;
    }}
    .process-card:hover {{ border-color: {gold}40; transform: translateY(-4px); }}
    .process-card::before {{
      content:''; position:absolute; top:0; left:0; right:0; height:2px;
      background: linear-gradient(90deg,transparent,{gold},transparent);
      opacity:0; transition: opacity 0.3s;
    }}
    .process-card:hover::before {{ opacity:1; }}
    .testimonial-card {{
      border: 1px solid {border}; border-radius: 16px; padding: 1.75rem;
      background: {feat_bg}; transition: all 0.28s;
    }}
    .testimonial-card:hover {{ border-color: {gold}30; transform: translateY(-3px); }}
    </style>
    """, unsafe_allow_html=True)

    # ── Build video/image source for hero ─────────────────────
    if has_video or has_video2:
        vsrc = ""
        if has_video:  vsrc += f'<source src="{VIDEO_URL}" type="video/mp4">'
        if has_video2: vsrc += f'<source src="{VIDEO_URL2}" type="video/mp4">'
        poster_attr = f'poster="{IMAGE_URL}"' if has_image else ""
        media_block = f'<div class="video-wrap"><video autoplay muted loop playsinline {poster_attr}>{vsrc}</video></div>'
    elif has_image:
        media_block = f'<div class="video-wrap" style="background:url({IMAGE_URL}) center/cover no-repeat"></div>'
    else:
        media_block = '<div class="grad-bg"></div><div class="orb1"></div><div class="orb2"></div><div class="orb3"></div>'

    # Theme toggle label
    toggle_label = "☀️ Light" if is_dark else "🌙 Dark"

    # ── Hero HTML ─────────────────────────────────────────────
    hero_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:{bg};font-family:'Inter',sans-serif;overflow-x:hidden}}

@keyframes fadeUp{{from{{opacity:0;transform:translateY(22px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes glow{{0%,100%{{opacity:.4}}50%{{opacity:.9}}}}
@keyframes gradDrift{{0%{{background-position:0% 50%}}50%{{background-position:100% 50%}}100%{{background-position:0% 50%}}}}
@keyframes floatA{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-16px)}}}}
@keyframes floatB{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-12px)}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:0.4}}}}

/* NAV */
.nav{{position:absolute;top:0;left:0;right:0;z-index:20;
  display:flex;align-items:center;justify-content:space-between;
  padding:1.3rem 6%;}}
.nav-logo{{font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:600;
  color:{text_p};letter-spacing:-.01em}}
.nav-logo em{{font-style:normal;color:{gold}}}
.nav-center{{display:flex;align-items:center;gap:8px;font-size:10px;font-weight:600;
  letter-spacing:.18em;text-transform:uppercase;color:{gold};
  background:{icon_bg};border:1px solid {gold}30;border-radius:100px;padding:5px 14px}}
.nav-theme{{width:34px;height:34px;border-radius:50%;background:{elevated};
  border:1px solid {border};display:flex;align-items:center;justify-content:center;
  font-size:15px;cursor:pointer;transition:all 0.2s}}

/* HERO */
.hero{{position:relative;width:100%;height:100vh;min-height:620px;overflow:hidden;background:{bg}}}
.video-wrap{{position:absolute;inset:0;z-index:0}}
.video-wrap video{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  min-width:100%;min-height:100%;object-fit:cover;opacity:0.42}}
.grad-bg{{position:absolute;inset:0;z-index:0;
  background:linear-gradient(135deg,{bg} 0%,#0d0d1a 40%,#111120 70%,{bg} 100%);
  background-size:400% 400%;animation:gradDrift 20s ease infinite}}
.orb1{{position:absolute;top:-10%;right:-6%;width:56vw;height:56vw;border-radius:50%;
  background:radial-gradient(circle,{orb1} 0%,transparent 68%);animation:glow 14s ease-in-out infinite}}
.orb2{{position:absolute;bottom:-14%;left:-10%;width:50vw;height:50vw;border-radius:50%;
  background:radial-gradient(circle,{orb2} 0%,transparent 65%)}}
.orb3{{position:absolute;top:40%;left:35%;width:28vw;height:28vw;border-radius:50%;
  background:radial-gradient(circle,{orb1} 0%,transparent 65%);animation:glow 18s ease-in-out infinite reverse}}

.overlay{{position:absolute;inset:0;z-index:1;
  background:linear-gradient(to bottom,
    rgba({overlay_rgb},.45) 0%,rgba({overlay_rgb},.2) 35%,
    rgba({overlay_rgb},.6) 72%,rgba({overlay_rgb},1) 100%)}}
.glow-accent{{position:absolute;inset:0;z-index:1;pointer-events:none;
  background:radial-gradient(ellipse 65% 75% at 55% 35%,{gold}09 0%,transparent 70%);
  animation:glow 16s ease-in-out infinite}}

/* CONTENT */
.content{{position:relative;z-index:2;height:100%;display:flex;
  flex-direction:column;justify-content:center;padding:0 8%;max-width:860px}}

.badge{{display:inline-flex;align-items:center;gap:7px;font-size:11px;font-weight:600;
  letter-spacing:.16em;text-transform:uppercase;color:{gold};background:{icon_bg};
  border:1px solid {gold}28;border-radius:100px;padding:5px 13px;margin-bottom:1.25rem;
  animation:fadeUp .7s ease .05s both}}
.badge-dot{{width:6px;height:6px;border-radius:50%;background:{gold};animation:pulse 2s ease-in-out infinite}}

.headline{{font-family:'Cormorant Garamond',serif;
  font-size:clamp(2.9rem,5.8vw,5.5rem);font-weight:600;line-height:1.07;
  color:{text_p};letter-spacing:-.025em;margin:0 0 1.4rem;
  animation:fadeUp .85s ease .12s both}}
.headline em{{font-style:italic;color:{gold_lt}}}

.subhead{{font-size:17px;color:{text_s};line-height:1.68;max-width:520px;
  margin-bottom:0;font-weight:300;animation:fadeUp .85s ease .25s both}}

/* STATS */
.stats{{display:flex;gap:2.5rem;flex-wrap:wrap;margin-top:2.8rem;padding-top:2rem;
  border-top:1px solid {border};animation:fadeUp .85s ease .4s both}}
.stat-num{{font-family:'Cormorant Garamond',serif;font-size:2.3rem;font-weight:700;
  color:{text_p};line-height:1;margin-bottom:5px}}
.stat-label{{font-size:10px;color:{text_m};text-transform:uppercase;letter-spacing:.13em}}

/* CTA BUTTONS inside hero */
.cta-row{{display:flex;align-items:center;gap:12px;margin-top:2.4rem;flex-wrap:wrap;
  animation:fadeUp .85s ease .32s both}}
.btn-primary{{display:inline-flex;align-items:center;gap:8px;
  background:linear-gradient(135deg,{gold},{gold_lt});color:#080810;
  font-family:'Inter',sans-serif;font-size:13px;font-weight:700;
  letter-spacing:.07em;text-transform:uppercase;text-decoration:none;
  padding:13px 28px;border-radius:10px;cursor:pointer;border:none;
  box-shadow:0 4px 22px {gold}45;transition:all 0.22s}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 8px 32px {gold}60}}
.btn-secondary{{display:inline-flex;align-items:center;
  background:transparent;color:{text_s};
  font-family:'Inter',sans-serif;font-size:13px;font-weight:500;
  text-decoration:none;padding:12px 22px;border-radius:10px;cursor:pointer;
  border:1px solid {border};transition:all 0.22s}}
.btn-secondary:hover{{border-color:{gold};color:{gold}}}
.btn-theme{{display:inline-flex;align-items:center;gap:6px;
  background:transparent;color:{text_m};
  font-family:'Inter',sans-serif;font-size:12px;font-weight:500;
  text-decoration:none;padding:11px 18px;border-radius:10px;cursor:pointer;
  border:1px solid {border};transition:all 0.22s}}
.btn-theme:hover{{border-color:{gold}55;color:{text_p}}}

/* FLOATING CARDS */
.float-card{{position:absolute;z-index:5;
  background:{card_bg};border:1px solid {border};border-radius:14px;
  padding:.85rem 1.2rem;backdrop-filter:blur(20px);
  box-shadow:0 12px 40px rgba(0,0,0,{'0.4' if is_dark else '0.12'})}}
.float-card-1{{right:7%;top:24%;animation:fadeUp .9s ease .6s both, floatA 6s ease-in-out 1.6s infinite}}
.float-card-2{{right:12%;bottom:26%;animation:fadeUp .9s ease .9s both, floatB 7s ease-in-out 1.9s infinite}}
.fc-label{{font-size:10px;color:{text_m};text-transform:uppercase;letter-spacing:.1em;margin-bottom:5px}}
.fc-value{{font-size:22px;font-weight:700;color:{text_p};font-family:'Cormorant Garamond',serif}}
.fc-green{{color:#3ECF8E;font-size:11px;margin-top:3px;font-weight:500}}
.fc-sub{{font-size:11px;color:{gold};margin-top:3px}}
.fc-dot{{display:inline-block;width:6px;height:6px;background:#3ECF8E;border-radius:50%;margin-right:4px}}

/* SCROLL HINT */
.scroll-hint{{position:absolute;bottom:1.8rem;left:50%;transform:translateX(-50%);
  display:flex;flex-direction:column;align-items:center;gap:6px;
  color:{text_m};font-size:9px;letter-spacing:.14em;text-transform:uppercase;
  animation:fadeUp 1.2s ease 1.2s both;z-index:5}}
@keyframes scrollPulse{{0%,100%{{opacity:.35;transform:scaleY(1)}}50%{{opacity:.7;transform:scaleY(1.2)}}}}
.scroll-line{{width:1px;height:30px;background:linear-gradient(to bottom,{text_m},transparent);
  animation:scrollPulse 2.2s ease-in-out infinite}}
</style>
</head>
<body>
<div class="hero">
{media_block}
<div class="overlay"></div>
<div class="glow-accent"></div>

<nav class="nav">
  <div class="nav-logo">PropScribe <em>AI</em></div>
  <div class="nav-center">🏠 Indian Real Estate</div>
  <div class="nav-theme">{toggle_label.split()[0]}</div>
</nav>

<div class="content">
  <div class="badge"><span class="badge-dot"></span> AI-Powered Property Listings</div>
  <div class="headline">List any property<br><em>in 10 seconds.</em></div>
  <div class="subhead">Professional listings for 99acres, MagicBricks &amp; WhatsApp.<br>
    In English, Hindi, or Marathi — built for Indian real estate agents.</div>

  <div class="cta-row">
    <button class="btn-primary" onclick="window.parent.postMessage({{type:'streamlit:setComponentValue',value:'signup'}},'*')">
      Get Started Free →
    </button>
    <button class="btn-secondary" onclick="window.parent.postMessage({{type:'streamlit:setComponentValue',value:'login'}},'*')">
      Sign In
    </button>
    <button class="btn-theme" onclick="window.parent.postMessage({{type:'streamlit:setComponentValue',value:'toggle_theme'}},'*')">
      {toggle_label}
    </button>
  </div>

  <div class="stats">
    <div><div class="stat-num">500+</div><div class="stat-label">Active Agents</div></div>
    <div><div class="stat-num">10K+</div><div class="stat-label">Listings Made</div></div>
    <div><div class="stat-num">3</div><div class="stat-label">Languages</div></div>
    <div><div class="stat-num">~10s</div><div class="stat-label">Avg. Time</div></div>
  </div>
</div>

<div class="float-card float-card-1">
  <div class="fc-label">Listings today</div>
  <div class="fc-value">1,247</div>
  <div class="fc-green"><span class="fc-dot"></span>Live &amp; growing</div>
</div>
<div class="float-card float-card-2">
  <div class="fc-label">Time saved</div>
  <div class="fc-value">2,080 hrs</div>
  <div class="fc-sub">vs manual writing</div>
</div>

<div class="scroll-hint"><div class="scroll-line"></div>Scroll</div>
</div>
</body>
</html>"""

    # Hero rendered with full HTML (video + buttons inside)
    result = components.html(hero_html, height=820, scrolling=False)

    # ── Streamlit buttons (hidden helpers for navigation from iframe) ──
    # We keep Streamlit buttons below as the actual navigation triggers
    # The iframe buttons visually take precedence; actual routing via these
    col_s, col_l, col_t, col_r = st.columns([0.2, 0.2, 0.18, 0.42])
    with col_s:
        if st.button("Get Started Free →", type="primary", key="landing_signup", use_container_width=True):
            st.session_state.page = "auth"
            st.session_state.auth_tab = "signup"
            st.rerun()
    with col_l:
        if st.button("Sign In", type="secondary", key="landing_login", use_container_width=True):
            st.session_state.page = "auth"
            st.session_state.auth_tab = "login"
            st.rerun()
    with col_t:
        tgl = "☀️ Light" if is_dark else "🌙 Dark"
        if st.button(tgl, key="theme_toggle_land", use_container_width=True):
            st.session_state.theme = "light" if is_dark else "dark"
            st.rerun()

    # ── FEATURES SECTION ─────────────────────────────────────
    md(f"""
    <div style="background:{section_bg};border-top:1px solid {border};padding:4.5rem 8% 0">
      <div style="text-align:center;margin-bottom:3rem">
        <div style="display:inline-flex;align-items:center;gap:10px;font-size:11px;font-weight:600;
                    letter-spacing:.18em;text-transform:uppercase;color:{gold};margin-bottom:1rem">
          <span style="width:22px;height:1px;background:{gold};display:inline-block"></span>
          What PropScribe Does
          <span style="width:22px;height:1px;background:{gold};display:inline-block"></span>
        </div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:clamp(1.8rem,3vw,2.7rem);
                    font-weight:600;color:{text_p};line-height:1.2;margin-bottom:.75rem">
          Everything an agent needs.<br><em style="color:{gold_lt}">One click.</em>
        </div>
        <div style="font-size:15px;color:{text_s};max-width:520px;margin:0 auto;line-height:1.65">
          Fill in property details, optionally upload a photo, choose your language — done.
        </div>
      </div>
    </div>
    """)

    c1, c2, c3 = st.columns(3)
    for col, icon, title, desc in zip(
        [c1, c2, c3],
        ["🏠", "🌐", "📷"],
        ["3 Formats, One Click", "3 Indian Languages", "Photo Intelligence"],
        [
            "Full listing, WhatsApp message, and email template — all generated in a single request. Ready to copy and paste anywhere.",
            "English, Hindi, and Marathi in proper Devanagari script. Reach every buyer in their preferred language.",
            "Upload a property photo. AI reads flooring, lighting, fixtures and weaves visual details into your listing automatically."
        ]
    ):
        with col:
            md(f"""
            <div class="feat-card" style="margin:.25rem 0 1.5rem;background:{feat_bg}">
              <div style="width:46px;height:46px;border-radius:12px;background:{icon_bg};
                          border:1px solid {gold}28;display:flex;align-items:center;
                          justify-content:center;font-size:22px;margin-bottom:1.1rem">{icon}</div>
              <div style="font-family:'Cormorant Garamond',serif;font-size:1.15rem;
                          font-weight:600;color:{text_p};margin-bottom:.55rem">{title}</div>
              <div style="font-size:13px;color:{text_s};line-height:1.72">{desc}</div>
            </div>
            """)

    # ── HOW IT WORKS ─────────────────────────────────────────
    md(f"""
    <div style="background:{section_bg};padding:4rem 8% 0;border-top:1px solid {border}">
      <div style="text-align:center;margin-bottom:2.5rem">
        <div style="display:inline-flex;align-items:center;gap:10px;font-size:11px;font-weight:600;
                    letter-spacing:.18em;text-transform:uppercase;color:{gold};margin-bottom:.9rem">
          <span style="width:22px;height:1px;background:{gold};display:inline-block"></span>
          How It Works
          <span style="width:22px;height:1px;background:{gold};display:inline-block"></span>
        </div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:clamp(1.8rem,3vw,2.6rem);
                    font-weight:600;color:{text_p}">
          4 steps. <em style="color:{gold_lt}">10 seconds.</em>
        </div>
      </div>
    </div>
    """)

    s1, s2, s3, s4 = st.columns(4)
    steps = [
        ("01","📝","Fill Details","Property type, area, location, price, floor, facing, amenities."),
        ("02","📷","Upload Photo","Optional. AI reads flooring, lighting, fixtures for richer listings."),
        ("03","🌐","Choose Language","English, Hindi, or Marathi — written end-to-end in that language."),
        ("04","⚡","Copy & Share","Paste on 99acres, MagicBricks, WhatsApp or email — zero editing."),
    ]
    for col, (num, icon, title, desc) in zip([s1, s2, s3, s4], steps):
        with col:
            md(f"""
            <div class="process-card" style="margin:.25rem 0 1.5rem;background:{feat_bg}">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem">
                <div style="width:38px;height:38px;border-radius:50%;background:{icon_bg};
                            border:1px solid {gold}30;display:flex;align-items:center;
                            justify-content:center;font-size:13px;font-weight:700;color:{gold};flex-shrink:0">{num}</div>
                <span style="font-size:18px">{icon}</span>
              </div>
              <div style="font-family:'Cormorant Garamond',serif;font-size:1.05rem;
                          font-weight:600;color:{text_p};margin-bottom:.5rem">{title}</div>
              <div style="font-size:12.5px;color:{text_s};line-height:1.68">{desc}</div>
            </div>
            """)

    # ── PLATFORM BADGES ───────────────────────────────────────
    badges_html = "".join([
        f'<span style="display:inline-flex;align-items:center;gap:7px;padding:.6rem 1.3rem;'
        f'border:1px solid {border};border-radius:100px;background:{card_bg};'
        f'font-size:13px;color:{text_s};font-weight:500;margin:.3rem">'
        f'<span style="font-size:16px">{ic}</span>{lb}</span>'
        for ic, lb in [("🏡","99acres"),("🔑","MagicBricks"),("🏘️","Housing.com"),
                       ("💬","WhatsApp"),("📧","Email"),("📱","Instagram DM")]
    ])
    md(f"""
    <div style="background:{section_bg};padding:3.5rem 8%;border-top:1px solid {border};text-align:center">
      <div style="display:inline-flex;align-items:center;gap:10px;font-size:11px;font-weight:600;
                  letter-spacing:.18em;text-transform:uppercase;color:{gold};margin-bottom:1rem">
        <span style="width:22px;height:1px;background:{gold};display:inline-block"></span>Works With
        <span style="width:22px;height:1px;background:{gold};display:inline-block"></span>
      </div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:clamp(1.6rem,2.6vw,2.2rem);
                  font-weight:600;color:{text_p};margin-bottom:1.75rem">Every platform agents use daily.</div>
      <div style="display:flex;flex-wrap:wrap;justify-content:center">{badges_html}</div>
    </div>
    """)

    # ── TESTIMONIALS ──────────────────────────────────────────
    md(f"""
    <div style="background:{section_bg};padding:4rem 8% 0;border-top:1px solid {border}">
      <div style="text-align:center;margin-bottom:2.5rem">
        <div style="display:inline-flex;align-items:center;gap:10px;font-size:11px;font-weight:600;
                    letter-spacing:.18em;text-transform:uppercase;color:{gold};margin-bottom:.9rem">
          <span style="width:22px;height:1px;background:{gold};display:inline-block"></span>Agent Reviews
          <span style="width:22px;height:1px;background:{gold};display:inline-block"></span>
        </div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:clamp(1.8rem,3vw,2.6rem);
                    font-weight:600;color:{text_p}">
          Loved by agents <em style="color:{gold_lt}">across India.</em>
        </div>
      </div>
    </div>
    """)
    t1, t2, t3 = st.columns(3)
    for col, name, role, stars, quote in zip(
        [t1, t2, t3],
        ["Rahul Sharma","Priya Mehta","Anil Kadam"],
        ["Senior Agent, Pune","Real Estate Broker, Mumbai","Property Consultant, Nashik"],
        ["⭐⭐⭐⭐⭐","⭐⭐⭐⭐⭐","⭐⭐⭐⭐⭐"],
        ['"PropScribe cut my listing time from 90 minutes to under a minute. The Marathi output is perfect for my local buyers."',
         '"The WhatsApp template is brilliant — I paste it directly into my broadcast list. Response rate up 40%."',
         '"Skeptical at first, but PropScribe nailed the Hindi listings. Even my clients noticed the quality improvement."']
    ):
        with col:
            md(f"""
            <div class="testimonial-card" style="margin:.25rem 0 1.5rem;background:{feat_bg}">
              <div style="font-size:14px;color:{text_s};line-height:1.72;margin-bottom:1.2rem;font-style:italic">{quote}</div>
              <div style="display:flex;align-items:center;gap:10px">
                <div style="width:36px;height:36px;border-radius:50%;background:{icon_bg};
                            border:1px solid {gold}30;display:flex;align-items:center;
                            justify-content:center;font-size:13px;font-weight:700;color:{gold}">{name[0]}</div>
                <div>
                  <div style="font-size:13px;font-weight:600;color:{text_p}">{name}</div>
                  <div style="font-size:11px;color:{text_m}">{role}</div>
                </div>
                <div style="margin-left:auto;font-size:11px">{stars}</div>
              </div>
            </div>
            """)

    # ── FINAL CTA ─────────────────────────────────────────────
    md(f"""
    <div style="background:{section_bg};padding:5rem 8%;border-top:1px solid {border};text-align:center">
      <div style="display:inline-flex;align-items:center;gap:10px;font-size:11px;font-weight:600;
                  letter-spacing:.18em;text-transform:uppercase;color:{gold};margin-bottom:1.25rem">
        <span style="width:22px;height:1px;background:{gold};display:inline-block"></span>Start For Free
        <span style="width:22px;height:1px;background:{gold};display:inline-block"></span>
      </div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:clamp(2rem,4vw,3.4rem);
                  font-weight:600;color:{text_p};line-height:1.15;margin-bottom:1rem">
        Your first 3 listings<br><em style="color:{gold_lt}">are completely free.</em>
      </div>
      <div style="font-size:15px;color:{text_s};max-width:440px;margin:0 auto 2.5rem;line-height:1.65">
        No credit card needed. Sign up in 30 seconds and start generating listings immediately.
      </div>
      <div style="display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap">
        <a href="#" style="display:inline-flex;align-items:center;gap:8px;
          background:linear-gradient(135deg,{gold},{gold_lt});color:#080810;
          font-family:'Inter',sans-serif;font-size:13px;font-weight:700;
          letter-spacing:.07em;text-transform:uppercase;text-decoration:none;
          padding:13px 32px;border-radius:10px;box-shadow:0 4px 22px {gold}45">
          Get Started Free →
        </a>
      </div>
    </div>
    """)
    _, cta_s, cta_l, _ = st.columns([0.28, 0.2, 0.15, 0.37])
    with cta_s:
        if st.button("Get Started →", type="primary", key="landing_cta_bottom", use_container_width=True):
            st.session_state.page = "auth"; st.session_state.auth_tab = "signup"; st.rerun()
    with cta_l:
        if st.button("Sign In", type="secondary", key="landing_login_bottom", use_container_width=True):
            st.session_state.page = "auth"; st.session_state.auth_tab = "login"; st.rerun()

    # ── FOOTER ────────────────────────────────────────────────
    md(f"""
    <div style="background:{surface};border-top:1px solid {border};
                padding:2.5rem 8%;display:flex;align-items:center;
                justify-content:space-between;flex-wrap:wrap;gap:1rem">
      <div style="font-family:'Cormorant Garamond',serif;font-size:19px;
                  font-weight:600;color:{text_p}">PropScribe<span style="color:{gold}"> AI</span></div>
      <div style="font-size:12px;color:{text_m}">© 2025 PropScribe AI · Built for Indian real estate agents</div>
      <div style="font-size:12px;color:{text_m}"><span style="color:{gold}">English</span> · हिंदी · मराठी</div>
    </div>
    """)