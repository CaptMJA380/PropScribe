# This function takes a dictionary of property details
# and returns a formatted prompt string for the LLM
# f-strings (f"...") let you embed Python variables inside strings
 
def build_listing_prompt(details: dict, language: str = "English") -> str:
    """
    Build a prompt that instructs GPT-4o to write a property listing.
    The more specific the prompt, the better the output.
    """
    
    amenities_str = ", ".join(details.get("amenities", []))
    
    prompt = f"""You are an expert Indian real estate agent with 10 years of experience 
selling properties in {details['location']}.
 
Write a professional property listing in {language} for the following property:
 
Property Type: {details['type']}
Location: {details['location']}  
Area: {details['area']} sqft
Price: Rs {details['price']}
Amenities: {amenities_str}
Floor: {details.get('floor', 'Not specified')}
Facing: {details.get('facing', 'Not specified')}
 
Your listing must include:
1. A compelling headline (max 10 words)
2. Three key highlights (one line each, start with a checkmark emoji)
3. A description paragraph (exactly 80-100 words, highlight location benefits)
4. A WhatsApp-ready short message (max 50 words)
5. A call to action
 
Tone: Professional, warm, and urgent. Avoid cliches like 'dream home'.
Write in {language} only. If Hindi or Marathi, use proper Devanagari script."""
 
    return prompt
 
 
def build_comparison_prompt(prop1: dict, prop2: dict) -> str:
    """Bonus: Compare two properties side by side (for later use)"""
    return f"""Compare these two properties for a buyer and recommend which 
is the better investment. Property 1: {prop1}. Property 2: {prop2}.
Give 3 reasons for your recommendation."""
