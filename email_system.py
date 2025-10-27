"""
Email automation system for Specks on Decks
Handles quote emails, confirmations, and reminders
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os

class EmailSystem:
    def __init__(self):
        # Configure your email settings here
        self.smtp_server = "smtp.gmail.com"  # Change if using different provider
        self.smtp_port = 587
        self.sender_email = os.getenv('BUSINESS_EMAIL', 'your-email@gmail.com')
        self.sender_password = os.getenv('EMAIL_PASSWORD', '')  # Use app password for Gmail
        self.admin_email = os.getenv('ADMIN_EMAIL', 'your-email@gmail.com')
        self.business_name = "Specks on Decks"

    def send_email(self, to_email, subject, html_content):
        """Send an email"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.business_name} <{self.sender_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Send email
            if self.sender_password:  # Only send if password is configured
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                server.quit()
                return True
            else:
                # For testing without email configured
                print(f"\n[EMAIL PREVIEW - Would send to {to_email}]")
                print(f"Subject: {subject}")
                print(f"Content: {html_content[:200]}...")
                return True

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_quote_email(self, booking_data, booking_id):
        """Send quote email to client"""
        subject = f"Your DJ Quote from {self.business_name}"

        # Build add-ons list
        addons_html = ""
        if booking_data.get('lighting_cost', 0) > 0:
            addons_html += f"<li>Lighting: £{booking_data['lighting_cost']:.2f}</li>"
        if booking_data.get('security_cost', 0) > 0:
            addons_html += f"<li>Security ({booking_data['security_hours']} hours @ £25/hr): £{booking_data['security_cost']:.2f}</li>"

        afterparty_note = ""
        if booking_data.get('has_afterparty'):
            afterparty_note = """
            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 2px; margin-top: 20px; border-left: 4px solid #000000;">
                <strong style="font-size: 1.1em; text-transform: uppercase; letter-spacing: 0.5px;">After Party Service Requested</strong><br><br>
                Venue rental, setup & coordination until 3am<br>
                <em>Custom quote will be provided via phone call</em>
            </div>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 0; }}
                .header {{ background: #000000; color: white; padding: 50px 30px; text-align: center; }}
                .header h1 {{ font-size: 2.5em; font-weight: 900; margin: 0 0 10px 0; letter-spacing: 2px; text-transform: uppercase; }}
                .header p {{ font-size: 1.2em; font-weight: 300; margin: 0; }}
                .content {{ background: #ffffff; padding: 40px 30px; }}
                .quote-box {{ background: #fafafa; padding: 25px; border-left: 4px solid #000000; margin: 20px 0; border-radius: 2px; }}
                .quote-box h3 {{ font-size: 1.3em; font-weight: 700; margin: 0 0 15px 0; text-transform: uppercase; letter-spacing: 1px; color: #000000; }}
                .total {{ font-size: 2em; font-weight: 900; color: #000000; margin-top: 15px; }}
                .footer {{ background: #0a0a0a; color: #999999; text-align: center; padding: 30px; font-size: 14px; }}
                ul {{ list-style: none; padding: 0; margin: 0; }}
                li {{ padding: 10px 0; border-bottom: 1px solid #e0e0e0; }}
                li:last-child {{ border-bottom: none; }}
                ol {{ padding-left: 20px; }}
                ol li {{ border-bottom: none; padding: 5px 0; }}
                hr {{ border: none; border-top: 2px solid #e0e0e0; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{self.business_name.upper()}</h1>
                    <p>Your Custom DJ Quote</p>
                </div>

                <div class="content">
                    <p>Hi {booking_data['client_name']},</p>

                    <p>Thank you for your interest in {self.business_name}! We're excited to potentially DJ your event.</p>

                    <div class="quote-box">
                        <h3>Event Details</h3>
                        <ul>
                            <li><strong>Event:</strong> {booking_data['event_type']}</li>
                            <li><strong>Date:</strong> {booking_data['event_date']}</li>
                            <li><strong>Time:</strong> {booking_data['event_time']}</li>
                            <li><strong>Location:</strong> {booking_data['location']}</li>
                            <li><strong>Guests:</strong> {booking_data['guest_count']}</li>
                            <li><strong>Duration:</strong> {booking_data['hours']} hours</li>
                        </ul>
                    </div>

                    <div class="quote-box">
                        <h3>Pricing Breakdown</h3>
                        <ul>
                            <li><strong>DJ Service (Base Rate):</strong> £{booking_data['base_price']:.2f}</li>
                            <li><strong>Travel Cost:</strong> £{booking_data['travel_cost']:.2f}</li>
                            {addons_html}
                        </ul>
                        <hr>
                        <p class="total">Total Quote: £{booking_data['total_quote']:.2f}</p>
                    </div>

                    {afterparty_note}

                    <p><strong>Next Steps:</strong></p>
                    <ol>
                        <li>Reply to this email or text us to confirm your booking</li>
                        <li>We'll send you a confirmation and contract</li>
                        <li>Pay a deposit to secure your date</li>
                        <li>Get ready to party! 🎉</li>
                    </ol>

                    <p>This quote is valid for 7 days. Our availability fills up quickly, so book soon!</p>

                    <p>Questions? Just reply to this email or give us a call.</p>

                    <p>Looking forward to making your event unforgettable!</p>

                    <p><strong>Lucas & Emile</strong><br>
                    {self.business_name}</p>
                </div>

                <div class="footer">
                    <p><strong style="color: #ffffff;">{self.business_name.upper()}</strong></p>
                    <p>Professional DJ Services</p>
                    <p style="margin-top: 15px; font-size: 12px;">Booking ID: #{booking_id}</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(booking_data['client_email'], subject, html_content)

    def send_admin_notification(self, booking_data, booking_id):
        """Send notification to admin about new booking inquiry"""
        subject = f"New Booking Inquiry #{booking_id} - {self.business_name}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .header {{ background: #000000; color: white; padding: 40px 30px; text-align: center; }}
                .header h1 {{ font-size: 1.8em; font-weight: 900; margin: 0; letter-spacing: 1px; text-transform: uppercase; }}
                .content {{ background: #ffffff; padding: 30px; }}
                .info-box {{ background: #fafafa; padding: 20px; border-left: 4px solid #000000; margin: 15px 0; }}
                .info-box p {{ margin: 8px 0; line-height: 1.6; }}
                .quote-total {{ font-size: 1.8em; font-weight: 900; color: #000000; margin: 20px 0; }}
                .button {{ display: inline-block; padding: 15px 35px; background: #000000; color: white; text-decoration: none; border-radius: 2px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>New Booking Inquiry</h1>
                </div>
                <div class="content">
                    <div class="info-box">
                        <p><strong>CLIENT INFORMATION</strong></p>
                        <p><strong>Name:</strong> {booking_data['client_name']}</p>
                        <p><strong>Email:</strong> {booking_data['client_email']}</p>
                        <p><strong>Phone:</strong> {booking_data.get('client_phone', 'Not provided')}</p>
                    </div>

                    <div class="info-box">
                        <p><strong>EVENT DETAILS</strong></p>
                        <p><strong>Type:</strong> {booking_data['event_type']}</p>
                        <p><strong>Date:</strong> {booking_data['event_date']}</p>
                        <p><strong>Time:</strong> {booking_data['event_time']}</p>
                        <p><strong>Location:</strong> {booking_data['location']}</p>
                        <p><strong>Guests:</strong> {booking_data['guest_count']}</p>
                    </div>

                    <div class="quote-total">Quote: £{booking_data['total_quote']:.2f}</div>

                    <p style="color: #666; margin: 20px 0;">Quote email has been automatically sent to the client.</p>

                    <a href="https://specksondecks.onrender.com/dashboard" class="button">View in Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(self.admin_email, subject, html_content)

    def send_confirmation_email(self, booking):
        """Send booking confirmation email"""
        subject = f"Booking Confirmed - {self.business_name}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 0 auto; }}
                .header {{ background: #000000; color: white; padding: 50px 30px; text-align: center; }}
                .header h1 {{ font-size: 2.5em; font-weight: 900; margin: 0 0 10px 0; letter-spacing: 2px; text-transform: uppercase; }}
                .header p {{ font-size: 1.2em; font-weight: 300; margin: 0; }}
                .content {{ background: #ffffff; padding: 40px 30px; }}
                .info-box {{ background: #fafafa; padding: 25px; border-left: 4px solid #000000; margin: 20px 0; border-radius: 2px; }}
                .info-box h3 {{ font-size: 1.3em; font-weight: 700; margin: 0 0 15px 0; text-transform: uppercase; letter-spacing: 1px; }}
                .info-box p {{ margin: 8px 0; line-height: 1.6; }}
                .footer {{ background: #0a0a0a; color: #999999; text-align: center; padding: 30px; font-size: 14px; }}
                ul {{ padding-left: 20px; line-height: 1.8; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>BOOKING CONFIRMED</h1>
                    <p>We're Ready to Make Your Event Unforgettable</p>
                </div>

                <div class="content">
                    <p>Hi {booking['client_name']},</p>

                    <p>Great news! Your booking with {self.business_name} is confirmed!</p>

                    <div class="info-box">
                        <h3>Event Details</h3>
                        <p><strong>Date:</strong> {booking['event_date']}</p>
                        <p><strong>Time:</strong> {booking['event_time']}</p>
                        <p><strong>Location:</strong> {booking['location']}</p>
                    </div>

                    <p><strong>What's Next?</strong></p>
                    <ul>
                        <li>We'll reach out closer to the date to confirm details</li>
                        <li>Feel free to send us your song requests anytime</li>
                        <li>We'll arrive 30 minutes early for setup</li>
                    </ul>

                    <p>We're excited to make your event amazing!</p>

                    <p><strong>Lucas & Emile</strong><br>{self.business_name}</p>
                </div>

                <div class="footer">
                    <p><strong style="color: #ffffff;">{self.business_name.upper()}</strong></p>
                    <p>Professional DJ Services</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.send_email(booking['client_email'], subject, html_content)

    def send_reminder_email(self, booking, days_until):
        """Send event reminder email"""
        if days_until == 7:
            subject = f"Your Event is in 1 Week! - {self.business_name}"
            message = "Just a friendly reminder that your event is coming up in one week!"
        elif days_until == 1:
            subject = f"See You Tomorrow! 🎉 - {self.business_name}"
            message = "Your event is tomorrow! We're all set and ready to go."
        else:
            subject = f"Event Reminder - {self.business_name}"
            message = f"Your event is in {days_until} days!"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>{message}</h2>

            <div style="background: #f9f9f9; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p><strong>Event:</strong> {booking['event_type']}</p>
                <p><strong>Date:</strong> {booking['event_date']}</p>
                <p><strong>Time:</strong> {booking['event_time']}</p>
                <p><strong>Location:</strong> {booking['location']}</p>
            </div>

            <p>Everything is set! If you have any last-minute questions or song requests, just reply to this email.</p>

            <p>See you soon!</p>

            <p><strong>Lucas & Emile</strong><br>{self.business_name}</p>
        </body>
        </html>
        """

        return self.send_email(booking['client_email'], subject, html_content)

    def send_payment_reminder(self, booking):
        """Send payment reminder email"""
        outstanding = booking['total_quote'] - booking['deposit_paid'] - booking['balance_paid']

        subject = f"Payment Reminder - {self.business_name}"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2>Payment Reminder</h2>

            <p>Hi {booking['client_name']},</p>

            <p>This is a friendly reminder about the outstanding balance for your upcoming event.</p>

            <div style="background: #f9f9f9; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p><strong>Event Date:</strong> {booking['event_date']}</p>
                <p><strong>Total Quote:</strong> £{booking['total_quote']:.2f}</p>
                <p><strong>Paid So Far:</strong> £{booking['deposit_paid'] + booking['balance_paid']:.2f}</p>
                <p><strong>Outstanding Balance:</strong> £{outstanding:.2f}</p>
            </div>

            <p>Please arrange payment before the event date. Reply to this email if you have any questions.</p>

            <p>Thank you!</p>

            <p><strong>Lucas & Emile</strong><br>{self.business_name}</p>
        </body>
        </html>
        """

        return self.send_email(booking['client_email'], subject, html_content)
