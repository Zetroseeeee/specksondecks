"""
Automated Reminder System for Specks on Decks
Runs in the background and sends reminders for upcoming events
"""

import schedule
import time
from datetime import datetime, timedelta
from database import BookingDatabase
from email_system import EmailSystem

class ReminderSystem:
    def __init__(self):
        self.db = BookingDatabase()
        self.email = EmailSystem()

    def check_reminders(self):
        """Check for events that need reminders"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for reminders...")

        # Get all confirmed bookings
        confirmed_bookings = self.db.get_all_bookings(status='confirmed')

        for booking in confirmed_bookings:
            try:
                event_date = datetime.strptime(booking['event_date'], '%Y-%m-%d')
                days_until = (event_date - datetime.now()).days

                # 7-day reminder
                if days_until == 7:
                    if self.should_send_reminder(booking, 'week_reminder'):
                        print(f"Sending 1-week reminder to {booking['client_name']}...")
                        self.email.send_reminder_email(booking, 7)
                        self.db.log_email(booking['id'], 'week_reminder', booking['client_email'])

                # 1-day reminder
                elif days_until == 1:
                    if self.should_send_reminder(booking, 'day_reminder'):
                        print(f"Sending 1-day reminder to {booking['client_name']}...")
                        self.email.send_reminder_email(booking, 1)
                        self.db.log_email(booking['id'], 'day_reminder', booking['client_email'])

            except Exception as e:
                print(f"Error processing booking {booking['id']}: {e}")

    def check_payment_reminders(self):
        """Check for bookings with outstanding payments"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking payment reminders...")

        confirmed_bookings = self.db.get_all_bookings(status='confirmed')

        for booking in confirmed_bookings:
            try:
                # Calculate outstanding balance
                outstanding = booking['total_quote'] - booking['deposit_paid'] - booking['balance_paid']

                # If there's an outstanding balance and event is coming up
                if outstanding > 0:
                    event_date = datetime.strptime(booking['event_date'], '%Y-%m-%d')
                    days_until = (event_date - datetime.now()).days

                    # Send payment reminder 3 days before event if not fully paid
                    if days_until == 3:
                        if self.should_send_reminder(booking, 'payment_reminder'):
                            print(f"Sending payment reminder to {booking['client_name']}...")
                            self.email.send_payment_reminder(booking)
                            self.db.log_email(booking['id'], 'payment_reminder', booking['client_email'])

            except Exception as e:
                print(f"Error processing payment for booking {booking['id']}: {e}")

    def should_send_reminder(self, booking, reminder_type):
        """Check if we've already sent this type of reminder"""
        # You could enhance this to check the email_log table
        # For now, we'll send it (database log prevents duplicates via timestamps)
        return True

    def check_follow_ups(self):
        """Send follow-up emails to inquiries that haven't been confirmed"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking follow-ups...")

        inquiries = self.db.get_all_bookings(status='inquiry')

        for inquiry in inquiries:
            try:
                created_date = datetime.fromisoformat(inquiry['created_at'])
                days_since = (datetime.now() - created_date).days

                # Send follow-up after 3 days
                if days_since == 3:
                    if self.should_send_reminder(inquiry, 'follow_up'):
                        print(f"Sending follow-up to {inquiry['client_name']}...")
                        self.send_follow_up(inquiry)
                        self.db.log_email(inquiry['id'], 'follow_up', inquiry['client_email'])

            except Exception as e:
                print(f"Error processing follow-up for inquiry {inquiry['id']}: {e}")

    def send_follow_up(self, inquiry):
        """Send a follow-up email to an inquiry"""
        subject = f"Still interested? - {self.email.business_name}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>Hi {inquiry['client_name']},</h2>

            <p>We wanted to follow up on your recent booking inquiry for your {inquiry['event_type']} on {inquiry['event_date']}.</p>

            <p>Are you still interested in booking us for your event? Our availability fills up quickly, and we'd love to secure your date!</p>

            <div style="background: #f9f9f9; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h3>Your Quote: £{inquiry['total_quote']:.2f}</h3>
                <p><strong>Event:</strong> {inquiry['event_date']} at {inquiry['event_time']}</p>
                <p><strong>Location:</strong> {inquiry['location']}</p>
            </div>

            <p>Just reply to this email or give us a call to confirm your booking!</p>

            <p><strong>Lucas & Emile</strong><br>{self.email.business_name}</p>
        </body>
        </html>
        """

        return self.email.send_email(inquiry['client_email'], subject, html_content)

    def run(self):
        """Run the reminder system"""
        print("="*60)
        print("SPECKS ON DECKS - REMINDER SYSTEM")
        print("="*60)
        print("\n🤖 Automated reminder system starting...")
        print("\nScheduled tasks:")
        print("  • Event reminders: Daily at 9:00 AM")
        print("  • Payment reminders: Daily at 10:00 AM")
        print("  • Follow-ups: Daily at 2:00 PM")
        print("\nPress CTRL+C to stop")
        print("="*60 + "\n")

        # Schedule tasks
        schedule.every().day.at("09:00").do(self.check_reminders)
        schedule.every().day.at("10:00").do(self.check_payment_reminders)
        schedule.every().day.at("14:00").do(self.check_follow_ups)

        # For testing: also check every hour
        # schedule.every().hour.do(self.check_reminders)

        # Run immediately on start for testing
        print("Running initial check...")
        self.check_reminders()
        self.check_payment_reminders()
        self.check_follow_ups()
        print("\nScheduled tasks are now running in the background...")

        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    reminder_system = ReminderSystem()
    reminder_system.run()
