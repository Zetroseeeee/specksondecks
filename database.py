"""
Database setup and models for Specks on Decks booking system
"""

import sqlite3
from datetime import datetime
import json

class BookingDatabase:
    def __init__(self, db_path='specksondecks.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT NOT NULL,
                client_email TEXT NOT NULL,
                client_phone TEXT,
                event_type TEXT NOT NULL,
                event_date TEXT NOT NULL,
                event_time TEXT NOT NULL,
                location TEXT NOT NULL,
                guest_count INTEGER,
                hours REAL,

                -- Pricing
                base_price REAL DEFAULT 100,
                travel_cost REAL DEFAULT 0,
                lighting_cost REAL DEFAULT 0,
                security_cost REAL DEFAULT 0,
                security_hours REAL DEFAULT 0,
                total_quote REAL,

                -- Add-ons
                has_lighting INTEGER DEFAULT 0,
                has_security INTEGER DEFAULT 0,
                has_afterparty INTEGER DEFAULT 0,
                afterparty_details TEXT,

                -- Status tracking
                status TEXT DEFAULT 'inquiry',
                payment_status TEXT DEFAULT 'pending',
                deposit_paid REAL DEFAULT 0,
                balance_paid REAL DEFAULT 0,

                -- Timestamps
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,

                -- Notes
                notes TEXT
            )
        ''')

        # Email log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id INTEGER,
                email_type TEXT NOT NULL,
                recipient TEXT NOT NULL,
                sent_at TEXT NOT NULL,
                status TEXT,
                FOREIGN KEY (booking_id) REFERENCES bookings (id)
            )
        ''')

        conn.commit()
        conn.close()

        # Run migrations
        self.run_migrations()

    def run_migrations(self):
        """Run database migrations for schema updates"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if afterparty_details column exists, add if not
        try:
            cursor.execute("SELECT afterparty_details FROM bookings LIMIT 1")
        except sqlite3.OperationalError:
            # Column doesn't exist, add it
            cursor.execute("ALTER TABLE bookings ADD COLUMN afterparty_details TEXT")
            conn.commit()

        conn.close()

    def add_booking(self, booking_data):
        """Add a new booking inquiry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.now().isoformat()

        cursor.execute('''
            INSERT INTO bookings (
                client_name, client_email, client_phone,
                event_type, event_date, event_time, location,
                guest_count, hours,
                base_price, travel_cost, lighting_cost, security_cost, security_hours,
                total_quote, has_lighting, has_security, has_afterparty, afterparty_details,
                status, payment_status, created_at, updated_at, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            booking_data['client_name'],
            booking_data['client_email'],
            booking_data.get('client_phone', ''),
            booking_data['event_type'],
            booking_data['event_date'],
            booking_data['event_time'],
            booking_data['location'],
            booking_data.get('guest_count', 0),
            booking_data.get('hours', 0),
            booking_data.get('base_price', 100),
            booking_data.get('travel_cost', 0),
            booking_data.get('lighting_cost', 0),
            booking_data.get('security_cost', 0),
            booking_data.get('security_hours', 0),
            booking_data.get('total_quote', 100),
            booking_data.get('has_lighting', 0),
            booking_data.get('has_security', 0),
            booking_data.get('has_afterparty', 0),
            booking_data.get('afterparty_details', ''),
            'inquiry',
            'pending',
            now,
            now,
            booking_data.get('notes', '')
        ))

        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return booking_id

    def get_all_bookings(self, status=None):
        """Get all bookings, optionally filtered by status"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if status:
            cursor.execute('SELECT * FROM bookings WHERE status = ? ORDER BY event_date DESC', (status,))
        else:
            cursor.execute('SELECT * FROM bookings ORDER BY event_date DESC')

        bookings = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return bookings

    def get_booking(self, booking_id):
        """Get a specific booking by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,))
        booking = cursor.fetchone()

        conn.close()

        return dict(booking) if booking else None

    def update_booking_status(self, booking_id, status):
        """Update booking status (inquiry, confirmed, completed, cancelled)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE bookings
            SET status = ?, updated_at = ?
            WHERE id = ?
        ''', (status, datetime.now().isoformat(), booking_id))

        conn.commit()
        conn.close()

    def update_payment(self, booking_id, deposit=None, balance=None):
        """Update payment information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if deposit is not None:
            cursor.execute('''
                UPDATE bookings
                SET deposit_paid = ?, updated_at = ?
                WHERE id = ?
            ''', (deposit, datetime.now().isoformat(), booking_id))

        if balance is not None:
            cursor.execute('''
                UPDATE bookings
                SET balance_paid = ?, updated_at = ?
                WHERE id = ?
            ''', (balance, datetime.now().isoformat(), booking_id))

        # Auto-update payment status
        booking = self.get_booking(booking_id)
        if booking:
            total_paid = booking['deposit_paid'] + booking['balance_paid']
            if total_paid >= booking['total_quote']:
                cursor.execute('''
                    UPDATE bookings
                    SET payment_status = 'paid'
                    WHERE id = ?
                ''', (booking_id,))
            elif total_paid > 0:
                cursor.execute('''
                    UPDATE bookings
                    SET payment_status = 'partial'
                    WHERE id = ?
                ''', (booking_id,))

        conn.commit()
        conn.close()

    def log_email(self, booking_id, email_type, recipient, status='sent'):
        """Log sent emails"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO email_log (booking_id, email_type, recipient, sent_at, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (booking_id, email_type, recipient, datetime.now().isoformat(), status))

        conn.commit()
        conn.close()

    def get_upcoming_events(self, days_ahead=7):
        """Get bookings happening in the next X days"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        from datetime import timedelta
        future_date = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        today = datetime.now().strftime('%Y-%m-%d')

        cursor.execute('''
            SELECT * FROM bookings
            WHERE status = 'confirmed'
            AND event_date >= ?
            AND event_date <= ?
            ORDER BY event_date ASC
        ''', (today, future_date))

        bookings = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return bookings
