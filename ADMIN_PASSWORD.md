# Admin Password Setup

The dashboard is now password-protected! Only people with the admin password can access it.

## Setting Your Admin Password

**On Render (Your Live Website):**

1. Go to https://dashboard.render.com
2. Click on your "specksondecks" service
3. Go to "Environment" tab
4. Click "Add Environment Variable"
5. Add:
   - **Key:** `ADMIN_PASSWORD`
   - **Value:** Your chosen password (make it strong!)
6. Click "Save Changes"
7. Render will automatically redeploy

## Accessing the Dashboard

1. Go to your website: `specksondecks.onrender.com`
2. Click "Admin Dashboard" button
3. Enter your admin password
4. You're in!

## Important:

- **Never share your admin password**
- The default password for local testing is `admin123`
- Always use a strong password on your live site
- You can change the password anytime by updating the environment variable

## Logging Out

- Click the "Logout" button in the top right of the dashboard
- This will log you out and redirect you to the home page

## If You Forget Your Password

1. Go to Render dashboard
2. Check the `ADMIN_PASSWORD` environment variable
3. Or change it to a new password
