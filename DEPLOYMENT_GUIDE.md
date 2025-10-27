# 🚀 Deploy Your Booking System Online

Get a real public URL like: `specksondecks.onrender.com`

## Option 1: Render (Recommended - Easiest & Free)

### Step 1: Create a GitHub Account (if you don't have one)
1. Go to https://github.com
2. Sign up for free

### Step 2: Push Your Code to GitHub

Open Terminal and run these commands:

```bash
cd /Users/emilemajed/specksondecks

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Specks on Decks booking system"

# Create a new repository on GitHub:
# Go to https://github.com/new
# Repository name: specksondecks
# Make it Public
# Click "Create repository"

# Then link and push (replace YOUR-USERNAME with your GitHub username):
git remote add origin https://github.com/YOUR-USERNAME/specksondecks.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Render

1. **Go to Render**: https://render.com
2. **Sign up** with your GitHub account (free)
3. **Click "New +"** → **"Web Service"**
4. **Connect your GitHub repository** (specksondecks)
5. **Configure:**
   - **Name:** specksondecks
   - **Region:** Choose closest to you
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
6. **Click "Create Web Service"**

### Step 4: Wait for Deployment (3-5 minutes)

Render will build and deploy your app. You'll get a URL like:
```
https://specksondecks.onrender.com
```

### Step 5: Access Your Site

- **Booking Form:** `https://specksondecks.onrender.com/book`
- **Dashboard:** `https://specksondecks.onrender.com/dashboard`

**Share the booking form link anywhere!**
- Instagram bio
- WhatsApp
- Social media
- Text messages

---

## Option 2: Railway (Alternative - Also Free & Easy)

1. **Go to Railway**: https://railway.app
2. **Sign up** with GitHub
3. **Click "New Project"** → **"Deploy from GitHub repo"**
4. **Select your specksondecks repository**
5. **Railway auto-detects everything!**
6. **Click the deployment** → **Settings** → **Generate Domain**
7. **Done!** You get a URL like `specksondecks.up.railway.app`

---

## Option 3: PythonAnywhere (Beginner-Friendly)

1. **Go to PythonAnywhere**: https://www.pythonanywhere.com
2. **Sign up** for free account
3. **Go to "Web" tab**
4. **Add a new web app**
5. **Choose Flask**
6. **Upload your files** using the file browser
7. **Configure** the WSGI file
8. **Reload** your web app
9. **Access at:** `yourusername.pythonanywhere.com`

Detailed guide: https://help.pythonanywhere.com/pages/Flask/

---

## Important Notes

### Free Tier Limitations:
- **Render/Railway**: App sleeps after 15 min of inactivity (takes 30 sec to wake up)
- **PythonAnywhere**: Always on but limited bandwidth
- **Solution for better uptime**: Upgrade to paid tier ($7/month) or use a "keep-alive" service

### Database:
- Your SQLite database will reset on Render/Railway when they restart
- **Solution**: Use PostgreSQL (free on Render/Railway)
- I can help you migrate to PostgreSQL if needed!

### Email Setup:
Once deployed, add environment variables in your hosting dashboard:
- `BUSINESS_EMAIL`: your-email@gmail.com
- `EMAIL_PASSWORD`: your-gmail-app-password
- `ADMIN_EMAIL`: your-email@gmail.com

---

## Custom Domain (Optional)

Want `book.specksondecks.com` instead of `.onrender.com`?

1. **Buy a domain** from Namecheap/GoDaddy ($10-15/year)
2. **Add custom domain** in Render/Railway settings
3. **Update DNS** records (they'll guide you)
4. **Done!** Professional URL

---

## Quick Test After Deployment

1. Visit your booking form URL
2. Fill it out with test data
3. Check your email for the quote
4. Check the dashboard to see the inquiry

---

## Need Help?

**Stuck on deployment?** Just let me know:
- Which platform you chose
- What error you're getting
- Screenshots help!

I'll walk you through it step by step.

---

## What's Next After Deployment?

1. ✅ Share booking link on Instagram
2. ✅ Add to WhatsApp status
3. ✅ Post on social media
4. ✅ Start getting automated bookings!
5. ✅ Watch the money roll in 💰

---

Built for Specks on Decks 🎧
