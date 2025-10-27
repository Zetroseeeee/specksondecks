# Email Setup Guide

Currently, the booking system saves all bookings to the database and displays them in your dashboard. Email notifications are configured but not yet active.

## To Enable Automatic Email Quotes:

1. **Get a Gmail App Password:**
   - Go to your Google Account settings
   - Enable 2-Factor Authentication if not already enabled
   - Go to Security → App Passwords
   - Generate an app password for "Mail"
   - Save this password securely

2. **Add Environment Variables in Render:**
   - Go to your Render dashboard: https://dashboard.render.com
   - Click on your "specksondecks" service
   - Go to "Environment" tab
   - Add these variables:
     - `BUSINESS_EMAIL`: your-email@gmail.com
     - `EMAIL_PASSWORD`: (your app password from step 1)
     - `ADMIN_EMAIL`: your-email@gmail.com (where you want booking notifications)

3. **Redeploy:**
   - After adding environment variables, click "Manual Deploy"
   - Emails will now be sent automatically!

## Current Status:

✅ Bookings are saved to database
✅ All bookings visible in dashboard
✅ Quotes calculated correctly
⏳ Email quotes (waiting for SMTP configuration)

## For Now:

When someone books:
1. Their booking appears in your dashboard at `/dashboard`
2. You can see all their details and the quote
3. Contact them manually via phone/email using the info in the dashboard
4. Mark bookings as "confirmed" or "completed" in the dashboard

Once you set up email (above), clients will automatically receive:
- Quote email immediately after booking
- Confirmation email when you mark as confirmed
- Payment reminders
