"""
main_app.py — PropScribe AI Main Application v2.1
Complete inline CSS for dark AND light mode — all Streamlit form overrides.
"""

import streamlit as st
from generate import generate_listing, describe_image
from auth import logout


def show_main_app():
    if "listing_count" not in st.session_state:
        st.session_state.listing_count = 0
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

    is_dark = st.session_state.theme == "dark"

    # Raw theme colors
    bg       = "#080810"      if is_dark else "#F5F2EC"
    surface  = "#0F0F1A"      if is_dark else "#FFFFFF"
    elevated = "#161625"      if is_dark else "#EDEAE2"
    card_bg  = "rgba(22,22,37,0.94)" if is_dark else "rgba(255,255,255,0.97)"
    border   = "rgba(255,255,255,0.07)" if is_dark else "rgba(0,0,0,0.09)"
    border_l = "rgba(255,255,255,0.12)" if is_dark else "rgba(0,0,0,0.15)"
    gold     = "#C9A348"      if is_dark else "#9F7625"
    gold_lt  = "#E8C56A"      if is_dark else "#B8892E"
    gold_glow = "rgba(201,163,72,0.11)" if is_dark else "rgba(159,118,37,0.08)"
    text_p   = "#F2EDE0"      if is_dark else "#1A1A2E"
    text_s   = "#9A9AAE"      if is_dark else "#4A4A68"
    text_m   = "#4A4A60"      if is_dark else "#8A8A9E"
    icon_bg  = "rgba(201,163,72,0.1)" if is_dark else "rgba(159,118,37,0.08)"
    sidebar_bg = "#0A0A14"    if is_dark else "#FFFFFF"
    sidebar_border = "rgba(255,255,255,0.05)" if is_dark else "rgba(0,0,0,0.07)"
    succ = "#3ECF8E"
    err  = "#F87171"

    # ── COMPLETE CSS with all raw values ──────────────────────
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;0,700;1,400;1,600&family=Inter:wght@300;400;500;600;700&display=swap');

    @keyframes fadeUp {{ from{{opacity:0;transform:translateY(14px)}} to{{opacity:1;transform:translateY(0)}} }}
    @keyframes pulse-success {{
      0%   {{ box-shadow: 0 0 0 0 rgba(62,207,142,0.4); }}
      70%  {{ box-shadow: 0 0 0 12px rgba(62,207,142,0); }}
      100% {{ box-shadow: 0 0 0 0 rgba(62,207,142,0); }}
    }}

    body, .stApp {{ background: {bg} !important; color: {text_p} !important; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
      background: {sidebar_bg} !important;
      border-right: 1px solid {sidebar_border} !important;
      display: block !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{ padding: 1.75rem 1.25rem !important; }}
    [data-testid="stSidebar"] .stMarkdown p {{
      color: {text_s} !important; font-size: 13px !important; line-height: 1.7 !important;
    }}
    [data-testid="stSidebar"] hr {{ border-color: {border} !important; margin: 1rem 0 !important; }}
    [data-testid="stSidebar"] a {{ color: {gold} !important; text-decoration: none !important; font-size: 13px !important; }}

    /* Main layout */
    .main .block-container {{ padding: 2rem 2.5rem 4rem !important; max-width: 1140px !important; }}
    hr {{ border: none !important; border-top: 1px solid {border} !important; margin: 1.5rem 0 !important; }}

    /* Form labels */
    .stTextInput > label, .stSelectbox > label,
    .stMultiSelect > label, .stFileUploader > label {{
      color: {text_s} !important; font-size: 11px !important;
      font-weight: 600 !important; text-transform: uppercase !important;
      letter-spacing: 0.1em !important;
    }}

    /* Text input */
    .stTextInput > div > div > input {{
      background: {elevated} !important; border: 1px solid {border_l} !important;
      border-radius: 10px !important; color: {text_p} !important;
      font-family: 'Inter', sans-serif !important; font-size: 14px !important;
      padding: 0.65rem 0.9rem !important;
    }}
    .stTextInput > div > div > input:focus {{
      border-color: {gold} !important; box-shadow: 0 0 0 3px {gold_glow} !important;
    }}
    .stTextInput > div > div > input::placeholder {{ color: {text_m} !important; }}

    /* Selectbox */
    .stSelectbox > div > div {{
      background: {elevated} !important; border: 1px solid {border_l} !important;
      border-radius: 10px !important; color: {text_p} !important;
    }}
    .stSelectbox > div > div > div {{ color: {text_p} !important; }}
    .stSelectbox > div > div:hover {{ border-color: {gold}55 !important; }}
    [data-baseweb="popover"] {{
      background: {elevated} !important; border: 1px solid {border} !important;
      border-radius: 10px !important;
    }}
    [data-baseweb="menu"] {{ background: {elevated} !important; }}
    [role="option"] {{ background: transparent !important; color: {text_s} !important; font-size: 14px !important; }}
    [role="option"]:hover, [aria-selected="true"] {{
      background: {gold_glow} !important; color: {gold} !important;
    }}

    /* Multiselect */
    .stMultiSelect > div > div {{
      background: {elevated} !important; border: 1px solid {border_l} !important;
      border-radius: 10px !important;
    }}
    .stMultiSelect > div > div:focus-within {{
      border-color: {gold} !important; box-shadow: 0 0 0 3px {gold_glow} !important;
    }}
    [data-baseweb="tag"] {{
      background: {gold_glow} !important; border-radius: 5px !important;
      color: {gold} !important; font-size: 12px !important;
    }}
    [data-baseweb="tag"] span {{ color: {gold} !important; }}

    /* File uploader */
    [data-testid="stFileUploader"] > div {{
      background: {elevated} !important; border: 1px dashed {gold}40 !important;
      border-radius: 14px !important; padding: 1.25rem !important;
    }}
    [data-testid="stFileUploader"] > div:hover {{ border-color: {gold}70 !important; background: {gold_glow} !important; }}

    /* Text area */
    .stTextArea > label {{ display: none !important; }}
    .stTextArea > div > div > textarea {{
      background: {elevated} !important; border: 1px solid {border_l} !important;
      border-radius: 10px !important; color: {text_p} !important;
      font-family: 'Inter', sans-serif !important; font-size: 13.5px !important;
      line-height: 1.72 !important; padding: 1rem !important;
    }}
    .stTextArea > div > div > textarea:focus {{
      border-color: {gold} !important; box-shadow: 0 0 0 3px {gold_glow} !important;
    }}

    /* Image */
    [data-testid="stImage"] img {{ border-radius: 10px !important; border: 1px solid {border} !important; }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
      background: {elevated} !important; border-radius: 10px !important;
      border-bottom: none !important; padding: 4px !important; gap: 4px !important;
    }}
    .stTabs [data-baseweb="tab"] {{
      background: transparent !important; color: {text_m} !important;
      font-family: 'Inter', sans-serif !important; font-size: 13px !important;
      border: none !important; border-radius: 7px !important;
      padding: 0.55rem 1.1rem !important;
    }}
    .stTabs [aria-selected="true"] {{
      background: {card_bg} !important; color: {gold} !important;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    }}
    .stTabs [data-baseweb="tab-panel"] {{ padding: 1.5rem 0 0 !important; }}

    /* Buttons */
    .stButton > button[kind="primary"] {{
      background: linear-gradient(135deg, {gold}, {gold_lt}) !important;
      color: #080810 !important; border: none !important; border-radius: 10px !important;
      font-family: 'Inter', sans-serif !important; font-size: 13px !important;
      font-weight: 700 !important; letter-spacing: 0.06em !important;
      text-transform: uppercase !important; padding: 0.75rem 1.5rem !important;
      box-shadow: 0 4px 20px {gold}40 !important; transition: all 0.22s !important;
    }}
    .stButton > button[kind="primary"]:hover {{
      transform: translateY(-2px) !important; box-shadow: 0 8px 30px {gold}55 !important;
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

    /* Spinner */
    .stSpinner > div > div {{ border-color: {gold} transparent transparent transparent !important; }}

    /* Markdown */
    .stMarkdown p {{ color: {text_s} !important; line-height: 1.7 !important; }}

    /* Section label class */
    .section-label {{
      font-size: 10px; font-weight: 700; letter-spacing: 0.14em;
      text-transform: uppercase; color: {text_m};
      margin-bottom: 1rem; padding-bottom: 0.5rem;
      border-bottom: 1px solid {border};
    }}
    .success-banner {{ animation: fadeUp 0.4s ease both, pulse-success 1.5s ease 0.4s; }}
    </style>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user", {})
    user_name  = user.get("name", "Agent")
    user_email = user.get("email", "")
    user_plan  = user.get("plan", "free")
    provider   = user.get("provider", "email")

    # ── SIDEBAR ────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style="margin-bottom:.5rem;padding-bottom:.75rem;border-bottom:1px solid {border}">
          <span style="font-family:'Cormorant Garamond',Georgia,serif;font-size:22px;
                       font-weight:600;color:{text_p}">PropScribe</span>
          <span style="font-family:'Cormorant Garamond',Georgia,serif;font-size:22px;
                       font-weight:400;color:{gold}"> AI</span>
          <div style="font-size:9px;color:{text_m};letter-spacing:.12em;text-transform:uppercase;margin-top:2px">
            Property Listing Generator
          </div>
        </div>
        """, unsafe_allow_html=True)

        initials = "".join(w[0].upper() for w in user_name.split()[:2])
        provider_badge = (
            f'<span style="font-size:9px;background:rgba(66,133,244,0.15);color:#4285F4;'
            f'padding:1px 6px;border-radius:4px;margin-left:6px">G</span>'
            if provider == "google" else ""
        )

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;background:{card_bg};
                    border:1px solid {border};border-radius:12px;padding:10px 12px;margin-bottom:8px">
          <div style="width:36px;height:36px;border-radius:50%;background:{icon_bg};
                      border:1px solid {gold}35;display:flex;align-items:center;
                      justify-content:center;font-size:13px;font-weight:600;color:{gold};flex-shrink:0">{initials}</div>
          <div style="overflow:hidden;flex:1">
            <div style="font-size:13px;font-weight:500;color:{text_p};white-space:nowrap;
                        overflow:hidden;text-overflow:ellipsis">{user_name}{provider_badge}</div>
            <div style="font-size:11px;color:{text_m};white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{user_email}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if user_plan == "free":
            st.markdown(f"""
            <div style="background:{icon_bg};border:1px solid {gold}22;border-radius:8px;
                        padding:7px 11px;margin-bottom:6px;
                        display:flex;align-items:center;justify-content:space-between">
              <span style="font-size:11px;color:{text_m}">Free plan</span>
              <span style="font-size:11px;color:{gold};font-weight:500">Upgrade →</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        used = st.session_state.listing_count
        remaining = max(0, 3 - used)
        pct = min(100, int((used / 3) * 100))
        bar_color = err if pct >= 100 else (gold if pct > 50 else succ)

        st.markdown(f"""
        <div style="margin-bottom:1rem">
          <div style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
                      color:{text_m};margin-bottom:10px">Session Usage</div>
          <div style="display:flex;align-items:baseline;gap:4px;margin-bottom:8px">
            <span style="font-family:'Cormorant Garamond',serif;font-size:2.4rem;font-weight:700;
                         color:{text_p};line-height:1">{used}</span>
            <span style="font-size:14px;color:{text_m}">/ 3 free</span>
          </div>
          <div style="height:4px;background:{border};border-radius:4px;overflow:hidden;margin-bottom:6px">
            <div style="height:100%;width:{pct}%;background:{bar_color};border-radius:4px;transition:width 0.5s ease"></div>
          </div>
          <div style="font-size:11px;color:{text_m}">{remaining} listing{'s' if remaining != 1 else ''} remaining</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown(f'<div style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{text_m};margin-bottom:12px">Quick Guide</div>', unsafe_allow_html=True)
        for num, icon, text in [("01","📝","Fill property details"),("02","📷","Upload a photo (optional)"),("03","🌐","Choose output language"),("04","⚡","Copy your listing")]:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">
              <div style="width:22px;height:22px;border-radius:50%;background:{elevated};
                          border:1px solid {border};display:flex;align-items:center;
                          justify-content:center;font-size:9px;font-weight:700;color:{gold};flex-shrink:0">{num}</div>
              <span style="font-size:12px;color:{text_s}">{icon} {text}</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        tgl = "☀️ Switch to Light" if is_dark else "🌙 Switch to Dark"
        if st.button(tgl, key="theme_toggle_app", use_container_width=True):
            st.session_state.theme = "light" if is_dark else "dark"; st.rerun()

        st.markdown(f"""
        <a href="https://forms.gle/REPLACE_WITH_YOUR_FORM_LINK"
           style="display:block;text-align:center;font-size:12px;color:{gold};text-decoration:none;
                  border:1px solid {gold}25;border-radius:8px;padding:7px 12px;margin-top:8px">
          Share feedback →
        </a>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
        if st.button("Sign out", type="secondary", use_container_width=True, key="logout_btn"):
            logout(); st.rerun()

    # ── UPGRADE WALL ───────────────────────────────────────────
    if st.session_state.listing_count >= 3:
        feats = ["Unlimited listings","English, Hindi & Marathi","All platforms","Priority support"]
        st.markdown(f"""
        <div style="padding:3.5rem 0;text-align:center">
          <div style="display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:600;
                      letter-spacing:.14em;text-transform:uppercase;color:{gold};margin-bottom:1.25rem">
            <span style="width:22px;height:1px;background:{gold};display:inline-block"></span>
            Free Tier Complete
            <span style="width:22px;height:1px;background:{gold};display:inline-block"></span>
          </div>
          <div style="font-family:'Cormorant Garamond',serif;font-size:2.5rem;font-weight:600;
                      color:{text_p};line-height:1.2;letter-spacing:-.02em;margin-bottom:1rem">
            You've used all 3 free listings.
          </div>
          <div style="font-size:15px;color:{text_s};max-width:480px;margin:0 auto 2rem;line-height:1.65">
            Upgrade to Pro for unlimited listings across all three languages.
          </div>
          <div style="display:flex;align-items:baseline;gap:8px;justify-content:center;margin-bottom:2rem">
            <span style="font-family:'Cormorant Garamond',serif;font-size:3.2rem;font-weight:700;color:{gold}">&#x20B9;499</span>
            <span style="font-size:14px;color:{text_m}">/month &middot; launch price</span>
            <span style="font-size:13px;color:{text_m};text-decoration:line-through">&#x20B9;999</span>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:.75rem;justify-content:center;margin-bottom:2rem">
            {"".join([f'<span style="display:flex;align-items:center;gap:6px;font-size:13px;color:{text_s}"><span style="color:{succ}">✓</span>{f}</span>' for f in feats])}
          </div>
          <a href="https://forms.gle/REPLACE_WITH_YOUR_FORM_LINK"
             style="display:inline-flex;align-items:center;gap:8px;
                    background:linear-gradient(135deg,{gold},{gold_lt});color:#080810;
                    font-family:'Inter',sans-serif;font-size:13px;font-weight:700;
                    letter-spacing:.06em;text-transform:uppercase;text-decoration:none;
                    padding:14px 36px;border-radius:10px;box-shadow:0 6px 28px {gold}40">
            Upgrade to Pro →
          </a>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # ── HERO HEADER ────────────────────────────────────────────
    st.markdown(f"""
    <div style="padding:2rem 0 1.5rem;animation:fadeUp .5s ease both">
      <div style="display:inline-flex;align-items:center;gap:8px;font-size:11px;font-weight:600;
                  letter-spacing:.16em;text-transform:uppercase;color:{gold};margin-bottom:.75rem">
        <span style="width:20px;height:1.5px;background:{gold};display:inline-block;border-radius:1px"></span>
        Welcome back, {user_name.split()[0]}
      </div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:clamp(2rem,3.5vw,2.8rem);
                  font-weight:600;color:{text_p};line-height:1.1;letter-spacing:-.02em;margin-bottom:.65rem">
        Generate your listing.
      </div>
      <div style="font-size:14px;color:{text_s};line-height:1.6">
        Fill in the details below — your professional listing is ready in ~10 seconds.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<hr style="border:none;border-top:1px solid {border};margin:0 0 1.5rem">', unsafe_allow_html=True)

    # ── INPUT FORM ─────────────────────────────────────────────
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(f'<div class="section-label" style="color:{text_m};border-bottom:1px solid {border}">🏠 Property Details</div>', unsafe_allow_html=True)
        prop_type = st.selectbox("Property type",
            ["2BHK Flat","3BHK Flat","1BHK Flat","4BHK Flat","Villa / Bungalow","Row House","Plot","Commercial Office","Shop / Showroom"])
        sub1, sub2 = st.columns(2)
        with sub1: area = st.text_input("Area (sqft)", placeholder="e.g. 950")
        with sub2: floor = st.text_input("Floor", placeholder="e.g. 4th of 8")
        location = st.text_input("Location", placeholder="e.g. Baner, Pune")

    with col2:
        st.markdown(f'<div class="section-label" style="color:{text_m};border-bottom:1px solid {border}">💰 Pricing & Features</div>', unsafe_allow_html=True)
        price = st.text_input("Price / Rent", placeholder="e.g. 85 lakhs or 25,000/mo")
        sub3, sub4 = st.columns(2)
        with sub3:
            facing = st.selectbox("Facing",["East","West","North","South","North-East","North-West","South-East","Not sure"])
        with sub4:
            language = st.selectbox("Language",["English","Hindi","Marathi"])
        amenities = st.multiselect("Amenities",
            ["Covered parking","Gym","Swimming pool","24hr security","Lift / Elevator","Power backup",
             "Garden / Terrace","CCTV","Clubhouse","Children play area","Jogging track","Intercom",
             "Solar panels","Rainwater harvesting","EV charging"], placeholder="Select amenities...")

    # ── PHOTO UPLOAD ───────────────────────────────────────────
    st.markdown(f'<hr style="border:none;border-top:1px solid {border};margin:1.25rem 0">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-label" style="color:{text_m};border-bottom:1px solid {border}">📷 Property Photo — Optional</div>', unsafe_allow_html=True)

    upload_col, preview_col = st.columns([2, 1])
    with upload_col:
        st.markdown(f'<div style="font-size:12px;color:{text_m};margin-bottom:.75rem;line-height:1.65">Upload a property photo and AI will describe flooring, lighting, fixtures and weave those details into your listing automatically.</div>', unsafe_allow_html=True)
        photo = st.file_uploader("Upload photo", type=["jpg","jpeg","png"], label_visibility="collapsed")

    photo_bytes = None
    if photo:
        photo_bytes = photo.read()
        with preview_col:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.image(photo_bytes, use_column_width=True)
            st.markdown(f'<div style="font-size:11px;color:{succ};text-align:center;margin-top:5px;display:flex;align-items:center;justify-content:center;gap:5px"><span style="width:6px;height:6px;border-radius:50%;background:{succ};display:inline-block"></span>Ready for AI analysis</div>', unsafe_allow_html=True)

    # ── GENERATE BUTTON ────────────────────────────────────────
    st.markdown(f'<hr style="border:none;border-top:1px solid {border};margin:1.25rem 0">', unsafe_allow_html=True)

    btn_col, meta_col = st.columns([1, 2])
    with btn_col:
        generate_clicked = st.button("⚡ Generate Listing →", type="primary", use_container_width=True)
    with meta_col:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:14px;padding:.6rem 0;flex-wrap:wrap">
          <div style="display:flex;align-items:center;gap:6px">
            <span style="width:6px;height:6px;border-radius:50%;background:{succ}"></span>
            <span style="font-size:12px;color:{text_m}"><span style="color:{gold};font-weight:600">{3 - st.session_state.listing_count}</span> free remaining</span>
          </div>
          <span style="color:{border};font-size:12px">&middot;</span>
          <span style="font-size:12px;color:{text_m}">~10 seconds</span>
          <span style="color:{border};font-size:12px">&middot;</span>
          <span style="font-size:12px;color:{text_m}"><span style="color:{text_p};font-weight:500">{language}</span> output</span>
          {f'<span style="color:{border};font-size:12px">&middot;</span><span style="font-size:12px;color:{succ}">📷 Photo attached</span>' if photo_bytes else ''}
        </div>
        """, unsafe_allow_html=True)

    # ── GENERATION LOGIC ───────────────────────────────────────
    if generate_clicked:
        errors = []
        if not area.strip():      errors.append("Built-up area is required")
        if not location.strip():  errors.append("Location is required")
        if len(location.strip()) > 200: errors.append("Location must be under 200 characters")
        if not price.strip():     errors.append("Price or rent is required")
        if len(price.strip()) > 100:    errors.append("Price field must be under 100 characters")

        if errors:
            for e in errors:
                st.markdown(f'<div style="background:rgba(248,113,113,0.1);border-left:3px solid {err};border-radius:8px;padding:10px 14px;margin-bottom:8px;font-size:13px;color:{err}">⚠️ {e}</div>', unsafe_allow_html=True)
            st.stop()

        spinner_msg = ("🔍 Analysing photo and crafting your listing..." if photo_bytes else "⚡ Writing your listing...")
        with st.spinner(spinner_msg):
            details = {
                "type": prop_type, "location": location.strip(), "area": area.strip(),
                "price": price.strip(), "floor": floor.strip() if floor else "Not specified",
                "facing": facing, "amenities": amenities, "photo_description": ""
            }
            if photo_bytes:
                details["photo_description"] = describe_image(photo_bytes, photo.type)
            result = generate_listing(details, language=language)
            st.session_state.last_result = result
            st.session_state.listing_count += 1

    # ── OUTPUT SECTION ─────────────────────────────────────────
    if st.session_state.last_result:
        result = st.session_state.last_result
        parts = result.split("---WHATSAPP---")
        full_listing = parts[0].strip()
        if len(parts) > 1:
            rest = parts[1].split("---EMAIL---")
            whatsapp_msg  = rest[0].strip()
            email_template = rest[1].strip() if len(rest) > 1 else full_listing
        else:
            whatsapp_msg  = full_listing
            email_template = full_listing

        st.markdown(f"""
        <div class="success-banner" style="display:flex;align-items:center;justify-content:space-between;
                    background:rgba(62,207,142,0.08);border:1px solid rgba(62,207,142,0.22);
                    border-radius:10px;padding:.9rem 1.2rem;margin:1.5rem 0 1rem">
          <div style="display:flex;align-items:center;gap:10px">
            <div style="width:8px;height:8px;border-radius:50%;background:{succ}"></div>
            <span style="font-size:13px;font-weight:500;color:{succ}">Listing generated in {language}</span>
          </div>
          <span style="font-size:11px;color:{text_m}">{st.session_state.listing_count} / 3 free used</span>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["🏠 Full Listing", "💬 WhatsApp", "📧 Email"])
        with tab1:
            st.markdown(f'<div style="font-size:11px;font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:{text_m};margin-bottom:.75rem">99acres · MagicBricks · Housing.com</div>', unsafe_allow_html=True)
            st.text_area("full", full_listing, height=300, key="out_full", label_visibility="collapsed")
        with tab2:
            st.markdown(f'<div style="font-size:11px;font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:{text_m};margin-bottom:.75rem">Paste into WhatsApp Broadcast</div>', unsafe_allow_html=True)
            st.text_area("wa", whatsapp_msg, height=200, key="out_wa", label_visibility="collapsed")
            st.markdown(f'<div style="font-size:11px;color:{text_m};margin-top:6px">Forward to your buyer enquiry list with zero editing needed.</div>', unsafe_allow_html=True)
        with tab3:
            st.markdown(f'<div style="font-size:11px;font-weight:600;letter-spacing:.11em;text-transform:uppercase;color:{text_m};margin-bottom:.75rem">Ready-to-Send Email</div>', unsafe_allow_html=True)
            st.text_area("email", email_template, height=280, key="out_email", label_visibility="collapsed")

        st.markdown(f"""
        <div style="margin-top:1.75rem;padding-top:1.25rem;border-top:1px solid {border};
                    display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
          <div style="font-size:13px;color:{text_m}">
            Need another?&nbsp;<span style="color:{gold};font-weight:500">{max(0, 3 - st.session_state.listing_count)} free remaining.</span>
          </div>
          <div style="font-size:12px;color:{text_m}">Scroll up to generate another listing ↑</div>
        </div>
        """, unsafe_allow_html=True)