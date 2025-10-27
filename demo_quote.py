#!/usr/bin/env python3
"""
Specks on Decks - Quote Generator Demo
Shows sample quote calculation
"""

from datetime import datetime

def calculate_quote(client_name, event_type, location, event_date, event_time,
                   guest_count, hours, travel_cost, add_lighting=False,
                   security_hours=0, afterparty=False):
    """Calculate quote with provided details"""

    # PRICING STRUCTURE
    base_dj_price = 100  # £100 flat rate

    # Optional add-ons
    lighting_cost = 75 if add_lighting else 0
    security_cost = security_hours * 25 if security_hours > 0 else 0

    # Calculate total
    total = base_dj_price + travel_cost + lighting_cost + security_cost

    # Display
    print("=" * 60)
    print("SPECKS ON DECKS - QUOTE GENERATOR")
    print("=" * 60)
    print()
    print("QUOTE BREAKDOWN")
    print("-" * 60)
    print(f"Client: {client_name}")
    print(f"Event: {event_type}")
    print(f"Date: {event_date} at {event_time}")
    print(f"Location: {location}")
    print(f"Duration: {hours} hours")
    print(f"Guest Count: {guest_count}")
    print("-" * 60)
    print()
    print("PRICING BREAKDOWN:")
    print("-" * 60)
    print(f"DJ Service (Base Rate): £{base_dj_price:.2f}")

    if travel_cost > 0:
        print(f"Travel Cost: £{travel_cost:.2f}")
    else:
        print(f"Travel Cost: £0.00")

    if lighting_cost > 0:
        print(f"Lighting: £{lighting_cost:.2f}")

    if security_cost > 0:
        print(f"Security ({security_hours} hours @ £25/hr): £{security_cost:.2f}")

    print("-" * 60)
    print(f"TOTAL QUOTE: £{total:.2f}")

    if afterparty:
        print("\n*** AFTER PARTY SERVICE REQUESTED ***")
        print("(Venue rental, setup & coordination until 3am)")
        print("Custom quote required - will be provided via phone call")

    print("=" * 60)
    print()

# Demo with sample events
print("\n" + "🎧" * 30)
print("DEMO: Here are some example quotes")
print("🎧" * 30 + "\n")

# Example 1: Basic package
print("\n📋 EXAMPLE 1: Basic Package (No Add-ons)\n")
calculate_quote(
    client_name="Sarah Johnson",
    event_type="18th Birthday Party",
    location="The Mill Venue, Local Town",
    event_date="15/11/2025",
    event_time="8:00 PM",
    guest_count=50,
    hours=4,
    travel_cost=0
)

# Example 2: With lighting
print("\n📋 EXAMPLE 2: With Lighting + Travel\n")
calculate_quote(
    client_name="Mike Thompson",
    event_type="Private Party",
    location="Garden Venue, Next City",
    event_date="22/11/2025",
    event_time="7:00 PM",
    guest_count=80,
    hours=5,
    travel_cost=15,
    add_lighting=True
)

# Example 3: Full package with security
print("\n📋 EXAMPLE 3: Full Package (Lighting + Security)\n")
calculate_quote(
    client_name="Emma Davis",
    event_type="21st Birthday Bash",
    location="Community Hall, Town Centre",
    event_date="23/11/2025",
    event_time="6:00 PM",
    guest_count=120,
    hours=6,
    travel_cost=20,
    add_lighting=True,
    security_hours=6
)

# Example 4: With after party service
print("\n📋 EXAMPLE 4: With After Party Service Request\n")
calculate_quote(
    client_name="Jack Wilson",
    event_type="18th Birthday",
    location="Private Venue",
    event_date="20/11/2025",
    event_time="9:00 PM",
    guest_count=100,
    hours=4,
    travel_cost=10,
    add_lighting=True,
    security_hours=4,
    afterparty=True
)

print("\n✅ To use the actual quote generator with your own inputs:")
print("   python3 /Users/emilemajed/specksondecks/quote_generator.py\n")
