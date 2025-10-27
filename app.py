"""
Specks on Decks - Automated Booking System
Flask web application for handling bookings, quotes, and tracking
Version: 2.0 - Professional Visual Design
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import BookingDatabase
from email_system import EmailSystem
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'specks-on-decks-secret-key-change-this'

# Initialize database and email system
db = BookingDatabase()
email_system = EmailSystem()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/book', methods=['GET'])
def booking_form():
    """Display booking form"""
    return render_template('booking_form.html')

@app.route('/api/quote', methods=['POST'])
def calculate_quote():
    """Calculate quote based on form data"""
    data = request.json

    # Base price
    base_price = 100

    # Travel cost
    travel_cost = float(data.get('travel_cost', 0))

    # Optional add-ons
    lighting_cost = 75 if data.get('add_lighting') else 0
    security_hours = float(data.get('security_hours', 0))
    security_cost = security_hours * 25

    # Calculate total
    total = base_price + travel_cost + lighting_cost + security_cost

    return jsonify({
        'base_price': base_price,
        'travel_cost': travel_cost,
        'lighting_cost': lighting_cost,
        'security_cost': security_cost,
        'security_hours': security_hours,
        'total': total,
        'has_afterparty': data.get('add_afterparty', False)
    })

@app.route('/api/submit-booking', methods=['POST'])
def submit_booking():
    """Handle booking form submission"""
    data = request.json

    try:
        # Prepare booking data
        booking_data = {
            'client_name': data['client_name'],
            'client_email': data['client_email'],
            'client_phone': data.get('client_phone', ''),
            'event_type': data['event_type'],
            'event_date': data['event_date'],
            'event_time': data['event_time'],
            'location': data['location'],
            'guest_count': int(data.get('guest_count', 0)),
            'hours': float(data.get('hours', 0)),
            'base_price': data['quote']['base_price'],
            'travel_cost': data['quote']['travel_cost'],
            'lighting_cost': data['quote']['lighting_cost'],
            'security_cost': data['quote']['security_cost'],
            'security_hours': data['quote']['security_hours'],
            'total_quote': data['quote']['total'],
            'has_lighting': 1 if data['quote']['lighting_cost'] > 0 else 0,
            'has_security': 1 if data['quote']['security_cost'] > 0 else 0,
            'has_afterparty': 1 if data['quote'].get('has_afterparty') else 0,
            'notes': data.get('notes', '')
        }

        # Save to database
        booking_id = db.add_booking(booking_data)

        # Send quote email to client
        email_sent = email_system.send_quote_email(booking_data, booking_id)

        # Send notification to you
        email_system.send_admin_notification(booking_data, booking_id)

        # Log emails
        if email_sent:
            db.log_email(booking_id, 'quote', booking_data['client_email'])
            db.log_email(booking_id, 'admin_notification', email_system.admin_email)

        return jsonify({
            'success': True,
            'booking_id': booking_id,
            'message': 'Booking inquiry received! Quote sent to your email.'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/dashboard')
def dashboard():
    """Admin dashboard to view all bookings"""
    # Get all bookings
    all_bookings = db.get_all_bookings()

    # Separate by status
    inquiries = [b for b in all_bookings if b['status'] == 'inquiry']
    confirmed = [b for b in all_bookings if b['status'] == 'confirmed']
    completed = [b for b in all_bookings if b['status'] == 'completed']

    # Calculate stats
    total_revenue = sum(b['total_quote'] for b in confirmed)
    pending_payments = sum(
        b['total_quote'] - b['deposit_paid'] - b['balance_paid']
        for b in confirmed
    )

    return render_template('dashboard.html',
                         inquiries=inquiries,
                         confirmed=confirmed,
                         completed=completed,
                         total_revenue=total_revenue,
                         pending_payments=pending_payments)

@app.route('/booking/<int:booking_id>')
def booking_detail(booking_id):
    """View details of a specific booking"""
    booking = db.get_booking(booking_id)
    if not booking:
        return "Booking not found", 404

    return render_template('booking_detail.html', booking=booking)

@app.route('/api/update-status/<int:booking_id>', methods=['POST'])
def update_status(booking_id):
    """Update booking status"""
    data = request.json
    new_status = data.get('status')

    if new_status not in ['inquiry', 'confirmed', 'completed', 'cancelled']:
        return jsonify({'success': False, 'error': 'Invalid status'}), 400

    db.update_booking_status(booking_id, new_status)

    # Send confirmation email if status changed to confirmed
    if new_status == 'confirmed':
        booking = db.get_booking(booking_id)
        email_system.send_confirmation_email(booking)
        db.log_email(booking_id, 'confirmation', booking['client_email'])

    return jsonify({'success': True})

@app.route('/api/update-payment/<int:booking_id>', methods=['POST'])
def update_payment(booking_id):
    """Update payment information"""
    data = request.json

    deposit = data.get('deposit')
    balance = data.get('balance')

    db.update_payment(booking_id, deposit=deposit, balance=balance)

    return jsonify({'success': True})

@app.route('/thank-you')
def thank_you():
    """Thank you page after booking submission"""
    return render_template('thank_you.html')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)

    print("\n" + "="*60)
    print("SPECKS ON DECKS - BOOKING SYSTEM")
    print("="*60)
    print("\nStarting server...")
    print("\n📋 Booking Form: http://localhost:5000/book")
    print("📊 Dashboard: http://localhost:5000/dashboard")
    print("\nPress CTRL+C to stop the server")
    print("="*60 + "\n")

    # Use environment variable for port (for deployment)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
