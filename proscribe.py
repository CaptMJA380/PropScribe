import time
from generate import generate_listing

# ── Test properties ───────────────────────────────────────────
# 3 different property types to verify your output
# In real usage, data comes from the web form in app.py
test_properties = [
    {
        "type": "2BHK Flat",
        "location": "Baner, Pune",
        "area": "950",
        "price": "85 lakhs",
        "floor": "4th floor of 8",
        "facing": "East",
        "amenities": ["Covered parking", "Gym", "24hr security", "Lift", "Power backup"],
        "photo_description": ""  # empty string — no photo in terminal test
    },
    {
        "type": "3BHK Villa",
        "location": "Wakad, Pune",
        "area": "1800",
        "price": "1.4 crore",
        "floor": "Ground + 1",
        "facing": "North-East",
        "amenities": ["Private garden", "2 car garage", "Swimming pool", "CCTV"],
        "photo_description": ""
    },
    {
        "type": "Commercial Office Space",
        "location": "Hinjewadi Phase 1, Pune",
        "area": "1200",
        "price": "75,000/mo rent",
        "floor": "6th floor",
        "facing": "West",
        "amenities": ["24hr access", "High-speed internet", "Reception", "Cafeteria"],
        "photo_description": ""
    }
]


# ── Main function ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print("PropScribe AI — Property Listing Generator")
    print("=" * 60)

    for i, prop in enumerate(test_properties, 1):
        print(f"\nGenerating listing {i} of {len(test_properties)}...")
        print(f"Property: {prop['type']} in {prop['location']}")
        print("-" * 60)

        listing = generate_listing(prop, language="English")
        print(listing)
        print("\n" + "=" * 60)

        # FIX: sleep is now INSIDE the loop between each listing
        # Original code had sleep AFTER the loop — which did nothing to
        # prevent rate limits between listings 1, 2, and 3
        if i < len(test_properties):
            print(f"\nWaiting 20 seconds before next request (rate limit protection)...")
            time.sleep(20)

    # Bonus: same property in Hindi
    print("\nBonus: generating listing in Hindi...")
    print("-" * 60)
    hindi_listing = generate_listing(test_properties[0], language="Hindi")
    print(hindi_listing)
    print("\nDone.")


# Only runs when you execute: python proscribe.py
# Will NOT run when app.py imports from generate.py
if __name__ == "__main__":
    main()