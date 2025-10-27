# 🚀 GET YOUR REAL WEBSITE URL - 10 MINUTES

Follow these exact steps to get your booking system online with a real URL.

## THE FASTEST WAY (Render - FREE)

### STEP 1: Create GitHub Account
1. Go to: https://github.com/signup
2. Sign up with your email
3. Verify your email

### STEP 2: Push Code to GitHub

Copy and paste these commands **ONE BY ONE** in your terminal:

```bash
cd /Users/emilemajed/specksondecks
```

```bash
git init
```

```bash
git add .
```

```bash
git commit -m "Specks on Decks booking system"
```

Now create a repository on GitHub:
1. Go to: https://github.com/new
2. **Repository name:** `specksondecks`
3. **Make it Public** (important!)
4. Click **"Create repository"**

Then run (replace `YOUR-GITHUB-USERNAME`):

```bash
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/specksondecks.git
```

```bash
git branch -M main
```

```bash
git push -u origin main
```

(Enter your GitHub username and password when asked)

### STEP 3: Deploy on Render

1. Go to: https://render.com
2. Click **"Get Started"**
3. Sign up with your GitHub account
4. Click **"New +"** (top right)
5. Select **"Web Service"**
6. Click **"Connect account"** to link GitHub
7. Find and select **"specksondecks"** repository
8. Fill in:
   - **Name:** `specksondecks`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
9. Click **"Create Web Service"**

### STEP 4: Wait (3-5 minutes)

Render will deploy your site. You'll see logs. Wait for:
```
✅ Deploy successful
```

### STEP 5: GET YOUR URL! 🎉

You'll see something like:
```
https://specksondecks.onrender.com
```

**Your URLs:**
- **Booking Form:** `https://specksondecks.onrender.com/book`
- **Dashboard:** `https://specksondecks.onrender.com/dashboard`

## SHARE IT EVERYWHERE!

✅ Instagram bio
✅ WhatsApp status
✅ Text to friends
✅ Social media posts

Anyone can now book you from anywhere in the world!

---

## TROUBLESHOOTING

### "git not found"
Install git:
```bash
brew install git
```

### "Permission denied"
Enter your GitHub username and password when prompted, or create a Personal Access Token

### "Build failed on Render"
Check that all files are committed:
```bash
git status
git add .
git commit -m "fix"
git push
```

### Need Help?
Just ask me! Share screenshots of any errors.

---

## Alternative: Even Easier Option

If GitHub/Render is too complex, use **Replit**:

1. Go to: https://replit.com
2. Sign up
3. Click **"Create Repl"**
4. Choose **"Import from GitHub"**
5. Or upload your files directly
6. Click **"Run"**
7. Replit gives you a URL instantly!

---

**You're 10 minutes away from having a real booking website!**

Let me know when it's live! 🚀
