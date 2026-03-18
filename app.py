import streamlit as st
from generate import generate_listing, describe_image

# ── Page config ──────────────────────────────────────────────
# Must be the very first Streamlit call in the script
st.set_page_config(
    page_title="PropScribe AI",
    page_icon="🏠",
    layout="wide"
)

# ── Session state initialisation ─────────────────────────────
# "not in" check means values only initialise on the very first load
# On every re-run after that, these lines are skipped
if "listing_count" not in st.session_state:
    st.session_state.listing_count = 0

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.title("PropScribe AI")
    st.caption("AI listing generator for Indian real estate agents")
    st.divider()

    st.metric(
        label="Free listings used",
        value=f"{st.session_state.listing_count} / 3"
    )
    st.divider()

    st.markdown("**How it works**")
    st.markdown("1. Fill in property details")
    st.markdown("2. Upload a photo (optional)")
    st.markdown("3. Click Generate")
    st.markdown("4. Copy your listing!")
    st.divider()

    st.markdown("**Feedback?**")
    # REPLACE THIS with your real Google Form URL before deploying
    st.markdown("[Fill our 1-minute form](https://forms.gle/REPLACE_WITH_YOUR_FORM_LINK)")

# ── Main header ───────────────────────────────────────────────
st.title("PropScribe AI 🏠")
st.caption("Generate professional property listings in seconds — English, Hindi, or Marathi")
st.divider()

# ── Input form ────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Property details")

    prop_type = st.selectbox(
        "Property type",
        ["2BHK Flat", "3BHK Flat", "1BHK Flat", "4BHK Flat",
         "Villa / Bungalow", "Row House", "Plot", "Commercial Office", "Shop / Showroom"]
    )

    area = st.text_input(
        "Built-up area (sqft)",
        placeholder="e.g. 950"
    )

    location = st.text_input(
        "Location",
        placeholder="e.g. Baner, Pune"
    )

    floor = st.text_input(
        "Floor",
        placeholder="e.g. 4th floor of 8"
    )

with col2:
    st.subheader("Pricing and features")

    price = st.text_input(
        "Price / Rent",
        placeholder="e.g. 85 lakhs or 25,000/mo"
    )

    facing = st.selectbox(
        "Facing direction",
        ["East", "West", "North", "South",
         "North-East", "North-West", "South-East", "Not sure"]
    )

    language = st.selectbox(
        "Output language",
        ["English", "Hindi", "Marathi"]
    )

    amenities = st.multiselect(
        "Amenities (select all that apply)",
        ["Covered parking", "Gym", "Swimming pool", "24hr security",
         "Lift / Elevator", "Power backup", "Garden / Terrace", "CCTV",
         "Clubhouse", "Children play area", "Jogging track", "Intercom",
         "Solar panels", "Rainwater harvesting", "EV charging"]
    )

# ── Photo upload ──────────────────────────────────────────────
st.divider()
st.subheader("Property photo (optional)")
st.caption("Upload a photo and AI will describe it and add visual details to your listing")

photo = st.file_uploader(
    "Upload photo",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

# FIX #2: Read bytes FIRST before st.image() consumes the file pointer
# In the original code st.image(photo) was called first, which moved the
# file pointer to the end — so photo.read() later returned empty bytes b""
# and describe_image() never actually received any image data.
photo_bytes = None
if photo:
    photo_bytes = photo.read()                             # read bytes first
    st.image(photo_bytes, caption="Photo preview", width=350)  # then display

# ── Generate button ───────────────────────────────────────────
st.divider()

# Check free tier limit — stop rendering if limit reached
if st.session_state.listing_count >= 3:
    st.warning("You have used all 3 free listings for this session.")
    st.markdown("### Want unlimited listings?")
    st.markdown("Join early access at our launch price of **Rs 499/month**:")
    # REPLACE THIS with your real Google Form URL before deploying
    st.markdown("[Get early access](https://forms.gle/REPLACE_WITH_YOUR_FORM_LINK)")
    st.stop()

if st.button("Generate listing", type="primary", use_container_width=True):

    # ── Input validation ──────────────────────────────────────
    # FIX #10 (future challenge): input length limits to prevent
    # prompt injection and runaway API costs
    if not area.strip():
        st.error("Please enter the property area (sqft).")
        st.stop()
    if not location.strip():
        st.error("Please enter the property location.")
        st.stop()
    if len(location.strip()) > 200:
        st.error("Location is too long. Please keep it under 200 characters.")
        st.stop()
    if not price.strip():
        st.error("Please enter the price or rent.")
        st.stop()
    if len(price.strip()) > 100:
        st.error("Price field is too long. Please keep it under 100 characters.")
        st.stop()

    # FIX #3: Single spinner only — Streamlit does not support nested spinners
    # Original code had a second st.spinner("Analysing photo...") nested inside
    # the outer spinner, which failed silently in Streamlit.
    spinner_msg = (
        "Analysing photo and writing your listing — about 15 seconds..."
        if photo_bytes
        else "Writing your listing — about 10 seconds..."
    )

    with st.spinner(spinner_msg):

        details = {
            "type": prop_type,
            "location": location.strip(),
            "area": area.strip(),
            "price": price.strip(),
            "floor": floor.strip() if floor else "Not specified",
            "facing": facing,
            "amenities": amenities,
            "photo_description": ""
        }

        # FIX #2: Use photo_bytes (already read above), not photo.read()
        # Also pass photo.type so describe_image() uses the correct MIME type
        # (FIX #7: original code always sent data:image/jpeg even for PNG files)
        if photo_bytes:
            details["photo_description"] = describe_image(photo_bytes, photo.type)

        result = generate_listing(details, language=language)

        st.session_state.last_result = result
        st.session_state.listing_count += 1

# ── Output section ────────────────────────────────────────────
# Runs on every re-run if a listing has been generated this session
if st.session_state.last_result:
    result = st.session_state.last_result

    # Split on separator markers from prompts.py
    parts = result.split("---WHATSAPP---")
    full_listing = parts[0].strip()

    if len(parts) > 1:
        rest = parts[1].split("---EMAIL---")
        whatsapp_msg = rest[0].strip()
        email_template = rest[1].strip() if len(rest) > 1 else full_listing
    else:
        # Fallback: GPT did not follow the separator format
        # Happens ~5% of the time — just click Generate again
        whatsapp_msg = full_listing
        email_template = full_listing

    st.divider()
    st.success(
        f"Listing generated! "
        f"({st.session_state.listing_count}/3 free listings used this session)"
    )

    tab1, tab2, tab3 = st.tabs(["Full listing", "WhatsApp message", "Email template"])

    with tab1:
        st.caption("Copy and paste to 99acres, MagicBricks, Housing.com, or any portal")
        st.text_area(
            "Full listing",
            full_listing,
            height=300,
            key="out_full",
            label_visibility="collapsed"
        )

    with tab2:
        st.caption("Paste directly into WhatsApp — ready to send to enquiries")
        st.text_area(
            "WhatsApp message",
            whatsapp_msg,
            height=180,
            key="out_wa",
            label_visibility="collapsed"
        )

    with tab3:
        st.caption("Ready-to-send email — just add your name and contact")
        st.text_area(
            "Email template",
            email_template,
            height=250,
            key="out_email",
            label_visibility="collapsed"
        )