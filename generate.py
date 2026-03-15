import openai
import base64
from config import OPENAI_API_KEY
from prompts import build_listing_prompt
 
# Create the OpenAI client once at module level
client = openai.OpenAI(api_key=OPENAI_API_KEY)
 
 
def generate_listing(details: dict, language: str = "English") -> str:
    """
    Unchanged from Week 1.
    Takes property details dict, returns formatted listing string.
    The prompt now includes photo_description if provided.
    """
    prompt = build_listing_prompt(details, language)
 
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional Indian real estate agent."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1000,   # Increased from 800 to fit 3 output formats
            temperature=0.7,
        )
        return response.choices[0].message.content
 
    except openai.AuthenticationError:
        return "Error: Invalid API key. Check your .env file."
    except openai.RateLimitError:
        return "Error: API rate limit hit. Wait 60 seconds and try again."
    except Exception as e:
        return f"Unexpected error: {str(e)}"
 
 
def describe_image(image_bytes: bytes) -> str:
    """
    NEW in Week 2.
    Sends a property photo to GPT-4o Vision and gets a description back.
    That description is injected into the listing prompt so the AI
    can mention specific visual details like flooring, lighting, and fixtures.
    
    Args:
        image_bytes: raw bytes from the uploaded photo file
    
    Returns:
        str: 2-3 sentence visual description, or "" if it fails
    """
 
    # Step 1: Convert image bytes to base64 string
    # base64.b64encode() takes bytes and returns bytes
    # .decode("utf-8") converts those bytes to a regular Python string
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
 
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Describe this property photo in 2-3 sentences for a real estate listing.
Focus on: room type, flooring material, lighting quality, key features or fixtures, and overall condition.
Be specific and factual. No exaggeration. Example style: 
'Spacious living room with vitrified tile flooring and large east-facing windows 
providing ample natural light. Features a false ceiling with recessed lighting and 
a modular TV unit with storage.'"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            }],
            max_tokens=150,
        )
        return response.choices[0].message.content
 
    except Exception:
        # If image description fails for any reason, return empty string
        # The listing will still generate — just without visual details
        return ""
 
 
def generate_listing_batch(properties: list, language: str = "English") -> list:
    """Unchanged from Week 1. Generate multiple listings at once."""
    return [generate_listing(prop, language) for prop in properties]
