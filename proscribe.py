from generate import generate_listing
import time 
# ============================================================
# TEST DATA — 3 different property types to test your output
# In real usage, this data will come from a web form (Week 2)
# ============================================================
 
test_properties = [
    {
        "type": "2BHK Flat",
          "location": "Baner, Pune",
        "area": "950",
        "price": "85 lakhs",
        "floor": "4th floor of 8",
        "facing": "East",
        "amenities": ["Covered parking", "Gym", "24hr security", "Lift", "Power backup"]
    },
    {
        "type": "3BHK Villa",
        "location": "Wakad, Pune",
        "area": "1800",
        "price": "1.4 crore",
        "floor": "Ground + 1",
        "facing": "North-East",
        "amenities": ["Private garden", "2 car garage", "Swimming pool", "CCTV"]
    },
    {
        "type": "Commercial Office Space",
        "location": "Hinjewadi Phase 1, Pune",
        "area": "1200",
        "price": "75,000/mo rent",
        "floor": "6th floor",
        "facing": "West",
        "amenities": ["24hr access", "High-speed internet", "Reception", "Cafeteria"]
    }
]
 
 
# ============================================================
# MAIN FUNCTION — runs when you type: python propscribe.py
# ============================================================
 
def main():
    print("=" * 60)
    print("PropScribe AI — Property Listing Generator")
    print("=" * 60)
    
    # Test all 3 property types
    for i, prop in enumerate(test_properties, 1):
        print(f"\nGenerating listing {i} of {len(test_properties)}...")
        print(f"Property: {prop['type']} in {prop['location']}")
        print("-" * 60)
        
        # Generate in English first
        listing = generate_listing(prop, language="English")
        print(listing)
        print("\n" + "=" * 60)
        
    # Bonus test — generate one listing in Hindi
    print("\nBonus: Same property in Hindi...")
    print("-" * 60)
    hindi_listing = generate_listing(test_properties[0], language="Hindi")
    print(hindi_listing)
    time.sleep(20)
 
# This is a Python convention:
# Code inside this block only runs when you run THIS file directly.
# It won't run if another file imports from propscribe.py
if __name__ == "__main__":
    main()

