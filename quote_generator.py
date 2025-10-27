#!/usr/bin/env python3
"""
Specks on Decks - Automated Quote Generator
Generates custom DJ quotes for private events
"""

from datetime import datetime
import math

def calculate_travel_cost(location):
    """
    Get actual travel cost (train ticket, cab fare, petrol, etc.)
    """
    print(f"\nLocation: {location}")
    travel_cost = float(input("Travel cost to get there (train/cab/petrol in £, enter 0 if none): £"))
    return travel_cost

def calculate_quote():
    """Main quote calculation function"""

    print("=" * 60)
    print("SPECKS ON DECKS - QUOTE GENERATOR")
    print("=" * 60)
    print()

    # Collect client information
    client_name = input("Client Name: ")
    event_type = input("Type of Event (e.g., 18th Birthday, Private Party): ")
    location = input("Event Location/Venue: ")
    event_date = input("Event Date (DD/MM/YYYY): ")
    event_time = input("Event Start Time (e.g., 8:00 PM): ")
    guest_count = int(input("Expected Guest Count: "))
    hours = float(input("Number of Hours Required: "))

    print("\n" + "=" * 60)

    # PRICING STRUCTURE
    # Base DJ service price
    base_dj_price = 100  # £100 flat rate

    # Travel cost
    travel_cost = calculate_travel_cost(location)

    # Optional add-ons
    print("\n--- OPTIONAL ADD-ONS ---")

    # Lighting
    add_lighting = input("Add lighting? (yes/no): ").lower() in ['yes', 'y']
    lighting_cost = 75 if add_lighting else 0

    # Security
    add_security = input("Add security? (yes/no): ").lower() in ['yes', 'y']
    security_hours = 0
    security_cost = 0
    if add_security:
        security_hours = float(input("How many hours of security needed?: "))
        security_cost = security_hours * 25  # £25/hour

    # After Party Service
    add_afterparty = input("After Party Service (venue rental, setup, coordination until 3am)? (yes/no): ").lower() in ['yes', 'y']
    afterparty_note = ""
    if add_afterparty:
        afterparty_note = "Custom quote - requires phone call"

    # Calculate total
    total = base_dj_price + travel_cost + lighting_cost + security_cost

    # Display itemized breakdown
    print("\n" + "=" * 60)
    print("\nQUOTE BREAKDOWN")
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

    if add_afterparty:
        print("\n*** AFTER PARTY SERVICE REQUESTED ***")
        print("(Venue rental, setup & coordination until 3am)")
        print("Custom quote required - will be provided via phone call")

    print("=" * 60)

    # Return all data for potential future use (saving to file, etc.)
    return {
        'client_name': client_name,
        'event_type': event_type,
        'location': location,
        'event_date': event_date,
        'event_time': event_time,
        'guest_count': guest_count,
        'hours': hours,
        'base_dj_price': base_dj_price,
        'travel_cost': travel_cost,
        'lighting_cost': lighting_cost,
        'security_cost': security_cost,
        'security_hours': security_hours,
        'afterparty_requested': add_afterparty,
        'total': total
    }

def main():
    """Run the quote generator"""
    while True:
        quote_data = calculate_quote()

        print("\n")
        another = input("Generate another quote? (yes/no): ").lower()
        if another not in ['yes', 'y']:
            print("\nThank you for using Specks on Decks Quote Generator!")
            break
        print("\n" * 2)

if __name__ == "__main__":
    main()
