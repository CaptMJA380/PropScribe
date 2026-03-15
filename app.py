import streamlit as st
from generate import generate_listing, describe_image
 
# ── Page config ─────────────────────────────────────────────
# Must be the very first Streamlit call in your script
# layout="wide" gives more horizontal space for the form
st.set_page_config(
    page_title="PropScribe AI",
    page_icon="🏠",
    layout="wide"
)
 
# ── Session state initialisation ────────────────────────────
# This block runs on every re-run, but "not in" check means
# it only sets the initial value on the very first load
if "listing_count" not in st.session_state:
    st.session_state.listing_count = 0  # How many listings generated
 
if "last_result" not in st.session_state:
    st.session_state.last_result = None  # The last generated listing text
 
# ── Sidebar ──────────────────────────────────────────────────
# Everything inside "with st.sidebar:" appears in the left panel
with st.sidebar:
    st.title("PropScribe AI")
    st.caption("AI listing generator for Indian real estate agents")
    st.divider()
 
    # st.metric shows a big number with a label above it
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
    st.markdown("[Fill our 1-minute form](https://forms.gle/yourlink)")
 
# ── Main header ──────────────────────────────────────────────
st.title("PropScribe AI 🏠")
st.caption("Generate professional property listings in seconds — English, Hindi, or Marathi")
st.divider()
 
# ── Input form ───────────────────────────────────────────────
# st.columns(2) splits the page into two equal halves
# "with col1:" means everything indented inside goes to the left column
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
 
# ── Photo upload ─────────────────────────────────────────────
st.divider()
st.subheader("Property photo (optional)")
st.caption("Upload a photo and AI will describe it and add visual details to your listing")
 
photo = st.file_uploader(
    "Upload photo",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)
 
# If photo was uploaded, show a preview
if photo:
    # st.image() displays an image in the app
    # width=350 limits the preview size
    st.image(photo, caption="Photo preview", width=350)
 
# ── Generate button ──────────────────────────────────────────
st.divider()
 
# Check free tier limit before showing the button
if st.session_state.listing_count >= 3:
    st.warning("You have used all 3 free listings for this session.")
    st.markdown("### Want unlimited listings?")
    st.markdown("Join early access at our launch price of **Rs 499/month**:")
    st.markdown("[Get early access](https://forms.gle/yourlink)")
    # st.stop() prevents anything below this from rendering
    st.stop()
 
# st.button() returns True only on the run where it was clicked
# So everything inside this if block runs exactly once per click
if st.button("Generate listing", type="primary", use_container_width=True):
 
    # Input validation — check required fields are not empty
    if not area.strip():
        st.error("Please enter the property area (sqft).")
        st.stop()
    if not location.strip():
        st.error("Please enter the property location.")
        st.stop()
    if not price.strip():
        st.error("Please enter the price or rent.")
        st.stop()
 
    # st.spinner() shows a loading animation while the indented block runs
    with st.spinner("Writing your listing — this takes about 10 seconds..."):
 
        # Build the property details dict
        # This is the exact same format as Week 1
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
 
        # If a photo was uploaded, describe it first
        # photo.read() gives us the raw bytes of the image file
        if photo:
            photo_bytes = photo.read()
            with st.spinner("Analysing photo..."):
                details["photo_description"] = describe_image(photo_bytes)
 
        # Call generate_listing — exact same function from Week 1
        result = generate_listing(details, language=language)
 
        # Store the result in session_state so it survives the next re-run
        st.session_state.last_result = result
 
        # Increment the usage counter
        st.session_state.listing_count += 1
 
# ── Output section ───────────────────────────────────────────
# This block runs on every re-run if there is a saved result
if st.session_state.last_result:
    result = st.session_state.last_result
 
    # Split the result into 3 parts using the separator markers
    # from our updated prompts.py
    parts = result.split("---WHATSAPP---")
    full_listing = parts[0].strip()
 
    if len(parts) > 1:
        rest = parts[1].split("---EMAIL---")
        whatsapp_msg = rest[0].strip()
        email_template = rest[1].strip() if len(rest) > 1 else full_listing
    else:
        # Fallback if GPT did not follow the separator format
        whatsapp_msg = full_listing
        email_template = full_listing
 
    st.divider()
    st.success(
        f"Listing generated! "
        f"({st.session_state.listing_count}/3 free listings used this session)"
    )
 
    # st.tabs() creates 3 clickable tabs
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
