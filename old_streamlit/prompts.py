def build_listing_prompt(details: dict, language: str = "English") -> str:
    """
    Builds the prompt for GPT-4o.
    Returns 3 formats separated by markers so app.py can split them into tabs.

    Output format:
    [Full listing here]
    ---WHATSAPP---
    [WhatsApp message here]
    ---EMAIL---
    [Email template here]
    """

    amenities_str = ", ".join(details.get("amenities", []))

    # Sanitise inputs to prevent prompt injection and runaway costs
    def sanitise(text: str, max_len: int = 200) -> str:
        return str(text).strip()[:max_len]

    # Include photo description if the agent uploaded a photo
    photo_section = ""
    if details.get("photo_description"):
        photo_section = f"\nPhoto description: {sanitise(details['photo_description'], 400)}"

    prompt = f"""You are an expert Indian real estate agent with 10 years of experience
selling properties in {sanitise(details['location'])}.{photo_section}

Write a professional property listing in {language} for:

Property Type: {sanitise(details['type'], 100)}
Location: {sanitise(details['location'])}
Area: {sanitise(details['area'], 50)} sqft
Price: Rs {sanitise(details['price'], 100)}
Amenities: {sanitise(amenities_str, 300)}
Floor: {sanitise(details.get('floor', 'Not specified'), 100)}
Facing: {sanitise(details.get('facing', 'Not specified'), 50)}

Return EXACTLY this structure with the separator lines included:

A compelling headline (max 10 words)

Three key highlights (one line each, start with checkmark emoji)

A description paragraph (exactly 80-100 words, highlight location benefits,
mention photo details if provided)

---WHATSAPP---
A WhatsApp-ready message (max 50 words, include price, location, 1 emoji,
end with: Call/WhatsApp me for site visit!)

---EMAIL---
Subject: [write subject line here]

Dear [Buyer Name],

[3 paragraph email: intro with key selling points, property details,
call to action with your contact]

Best regards,
[Agent Name]
PropScribe Realty

Tone: Professional, warm, urgent. No cliches like 'dream home' or 'prime location'.
Write entirely in {language}. If Hindi or Marathi, use proper Devanagari script."""

    return prompt


def build_comparison_prompt(prop1: dict, prop2: dict) -> str:
    """Bonus: Compare two properties side by side (for future use)"""
    return f"""Compare these two properties for a buyer and recommend which
is the better investment. Property 1: {prop1}. Property 2: {prop2}.
Give 3 specific reasons for your recommendation."""