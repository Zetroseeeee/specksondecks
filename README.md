# Specks on Decks - Automated Booking System

Complete automated booking, quoting, and management system for your DJ business.

## Features

### 1. Automated Booking Form + Quote System
- Beautiful web form for clients to request bookings
- Instant quote calculation based on your pricing
- Automatically emails professional quote to client
- Sends you a notification for each new inquiry
- All inquiries saved to database

### 2. Dashboard to Track Everything
- View all inquiries, confirmed bookings, and completed events
- Track payment status (pending, partial, paid)
- See total revenue and pending payments
- Update booking status with one click
- All your business data in one place

### 3. Automated Email Reminders
- **Follow-ups:** Automatically follows up with inquiries after 3 days
- **7-day reminder:** Sends reminder to clients 1 week before event
- **1-day reminder:** Sends "see you tomorrow" email
- **Payment reminders:** Reminds clients about outstanding balances
- Runs in the background 24/7

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/emilemajed/specksondecks
pip3 install -r requirements.txt
```

### 2. Start the Booking System

Open a terminal and run:

```bash
cd /Users/emilemajed/specksondecks
python3 app.py
```

This starts the web server. You'll see:
- **Booking Form:** http://localhost:5000/book
- **Dashboard:** http://localhost:5000/dashboard

### 3. Start the Reminder System (Optional)

Open a **second** terminal and run:

```bash
cd /Users/emilemajed/specksondecks
python3 reminder_system.py
```

This runs in the background and sends automated emails.

## How to Use

### For Clients (Public Booking Form)

1. Go to http://localhost:5000/book
2. Fill out their event details
3. Add optional services (lighting, security, after party)
4. Click "Calculate Quote" to see instant pricing
5. Click "Submit" - they instantly receive a professional email quote

### For You (Admin Dashboard)

1. Go to http://localhost:5000/dashboard
2. See all new inquiries
3. Click "Confirm Booking" when they agree
4. Track payments
5. Mark events as completed

## Email Setup (Optional but Recommended)

To enable automatic emails, set up your Gmail:

1. **Get a Gmail App Password:**
   - Go to your Google Account settings
   - Security > 2-Step Verification (enable it)
   - Security > App passwords
   - Generate a password for "Mail"

2. **Set Environment Variables:**

```bash
export BUSINESS_EMAIL="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export ADMIN_EMAIL="your-email@gmail.com"
```

Or add to your `~/.zshrc` file:

```bash
export BUSINESS_EMAIL="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export ADMIN_EMAIL="your-email@gmail.com"
```

Then run: `source ~/.zshrc`

**Note:** Without email setup, the system still works! It will just print emails to the terminal instead of sending them.

## Pricing Configuration

Your current pricing (can be customized in `app.py` and `email_system.py`):

- **Base DJ Service:** £100
- **Travel:** Actual cost (entered manually)
- **Lighting:** £75
- **Security:** £25/hour
- **After Party Service:** Custom quote (flagged for phone call)

## File Structure

```
specksondecks/
├── app.py                    # Main web application
├── database.py               # Database management
├── email_system.py           # Email automation
├── reminder_system.py        # Automated reminders
├── quote_generator.py        # Original CLI quote tool
├── requirements.txt          # Python dependencies
├── specksondecks.db         # Database (created automatically)
├── templates/
│   ├── booking_form.html    # Public booking form
│   ├── dashboard.html       # Admin dashboard
│   └── thank_you.html       # Success page
└── static/                   # Static files (CSS, images)
```

## Sharing Your Booking Form

### Option 1: Test Locally (for now)
- Clients can only access on your computer: http://localhost:5000/book

### Option 2: Share on Your Network
1. Find your local IP address:
   ```bash
   ifconfig | grep "inet "
   ```
2. Share link: `http://YOUR-IP:5000/book` (e.g., http://192.168.1.100:5000/book)
3. Works for anyone on the same WiFi

### Option 3: Make it Public (Future)
To make it accessible from anywhere:
- Deploy to Heroku (free)
- Deploy to PythonAnywhere (free)
- Deploy to Vercel/Netlify (free)
- Buy a domain and host it

I can help you set this up later!

## Tips

### Share Booking Link
- Add to Instagram bio
- Add to WhatsApp status
- Send directly to potential clients
- Add to social media posts

### Use the Dashboard Daily
- Check for new inquiries every morning
- Follow up with inquiries personally
- Update payment status when you receive money
- Mark events complete after you perform

### Let Automation Do the Work
- Quotes are sent automatically - no manual work!
- Reminders are sent automatically - never forget!
- All data is saved - no more lost conversations

## Troubleshooting

### "Port already in use"
If you see an error about port 5000:
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9

# Then start again
python3 app.py
```

### Database Issues
If you need to reset the database:
```bash
rm specksondecks.db
python3 app.py  # Will create fresh database
```

### Emails Not Sending
- Check environment variables are set
- Make sure you're using Gmail App Password (not regular password)
- Check spam folder
- Without email setup, quotes print to terminal (still works!)

## What's Next?

Want to add more features? Here are ideas:
- Client song request portal
- Automated contracts/invoices
- Online payment integration (Stripe/PayPal)
- Availability calendar
- Instagram integration
- SMS reminders via Twilio
- Analytics dashboard

Just let me know what you want next!

## Support

Having issues or want to add features? Just ask!

---

Built for **Specks on Decks** - Making booking management effortless 🎧
