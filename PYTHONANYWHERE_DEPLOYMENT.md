# Deploy to PythonAnywhere - Complete Guide

This guide will walk you through deploying your SoftProject API to PythonAnywhere.

---

## 📋 Prerequisites

- [x] PythonAnywhere account (free tier works!)
- [x] Your project code ready
- [x] GitHub account (recommended for easy deployment)

---

## 🚀 Deployment Steps

### Step 1: Create PythonAnywhere Account

1. Go to [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)
2. Click **"Start running Python online in less than a minute!"**
3. Choose **"Create a Beginner account"** (Free)
4. Fill in your details and create account
5. Verify your email

---

### Step 2: Upload Your Project

#### Option A: Using GitHub (Recommended)

1. **Push your project to GitHub:**

```bash
# In your project directory
git init
git add .
git commit -m "Initial commit for deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/SoftProject_api.git
git branch -M main
git push -u origin main
```

2. **Clone on PythonAnywhere:**

- Go to PythonAnywhere Dashboard
- Click **"Consoles"** → **"Bash"**
- Run:

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/SoftProject_api.git
cd SoftProject_api
```

#### Option B: Upload Files Manually

1. Go to **"Files"** tab in PythonAnywhere
2. Create directory: `SoftProject_api`
3. Upload all your files:
   - `api/` folder
   - `frontend/` folder
   - `softproject_api/` folder
   - `manage.py`
   - `requirements.txt`
   - `db.sqlite3` (if you want existing data)

---

### Step 3: Create Virtual Environment

In the Bash console:

```bash
cd ~/SoftProject_api

# Create virtual environment
python3.10 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your prompt
```

---

### Step 4: Install Dependencies

```bash
# Make sure you're in the virtual environment
pip install --upgrade pip
pip install -r requirements.txt
```

**If you get errors**, install manually:

```bash
pip install django djangorestframework django-cors-headers
```

---

### Step 5: Update Django Settings for Production

Create a new settings file for production:

```bash
nano ~/SoftProject_api/softproject_api/settings_production.py
```

Copy and paste this configuration:

```python
# Import all settings from base settings
from .settings import *

# SECURITY WARNING: change this in production!
SECRET_KEY = 'your-new-secret-key-change-this-to-something-random'

# Debug should be False in production (but we'll keep it True for easier debugging initially)
DEBUG = True  # Change to False after everything works

# Add your PythonAnywhere domain
ALLOWED_HOSTS = [
    'your-username.pythonanywhere.com',
    'www.your-username.pythonanywhere.com',
]

# Update CORS for your domain
CORS_ALLOWED_ORIGINS = [
    'https://your-username.pythonanywhere.com',
    'http://your-username.pythonanywhere.com',
]

CORS_ALLOW_ALL_ORIGINS = False  # More secure
CORS_ALLOW_CREDENTIALS = True

# Database - SQLite works fine for small projects
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For development, keep password validation disabled
AUTH_PASSWORD_VALIDATORS = []
```

**Important**: Replace `your-username` with your actual PythonAnywhere username!

Press `Ctrl+O` to save, `Enter` to confirm, `Ctrl+X` to exit.

---

### Step 6: Set Up the Database

```bash
cd ~/SoftProject_api
source venv/bin/activate

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Initialize services (Electricity, Water, Gas)
python manage.py init_services

# Create a superuser (admin account)
python manage.py createsuperuser
# Enter username, mobile number, password when prompted
```

---

### Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

### Step 8: Create Web App on PythonAnywhere

1. Go to **"Web"** tab in PythonAnywhere Dashboard
2. Click **"Add a new web app"**
3. Click **"Next"**
4. Choose **"Manual configuration"** (NOT Django wizard)
5. Choose **Python 3.10**
6. Click **"Next"**

---

### Step 9: Configure the Web App

#### 9.1 Set Virtual Environment Path

In the **Web** tab, find **"Virtualenv"** section:

- Click the text that says "Enter path to a virtualenv..."
- Enter: `/home/YOUR_USERNAME/SoftProject_api/venv`
- Replace `YOUR_USERNAME` with your actual username

#### 9.2 Configure WSGI File

1. In the **Web** tab, find **"Code"** section
2. Click on the **WSGI configuration file** link (something like `/var/www/your_username_pythonanywhere_com_wsgi.py`)
3. **Delete all the content** and replace with:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOUR_USERNAME/SoftProject_api'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable to tell Django where settings are
os.environ['DJANGO_SETTINGS_MODULE'] = 'softproject_api.settings_production'

# Activate virtual environment
activate_this = '/home/YOUR_USERNAME/SoftProject_api/venv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Important**: Replace `YOUR_USERNAME` with your actual PythonAnywhere username!

Save the file (Ctrl+S or click Save).

#### 9.3 Configure Static Files Mapping

In the **Web** tab, find **"Static files"** section:

Add these mappings:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/SoftProject_api/staticfiles/` |
| `/frontend/` | `/home/YOUR_USERNAME/SoftProject_api/frontend/` |

**Important**: Replace `YOUR_USERNAME` with your actual username!

---

### Step 10: Reload Web App

1. Go to the top of the **Web** tab
2. Click the big green **"Reload your-username.pythonanywhere.com"** button
3. Wait for it to finish

---

### Step 11: Test Your Deployment

1. Visit: `https://your-username.pythonanywhere.com/`
   - You should see your frontend

2. Test API: `https://your-username.pythonanywhere.com/api/services/`
   - Should return JSON with services

3. Test Debug endpoint: `https://your-username.pythonanywhere.com/api/debug/users/`
   - Should show user list

---

## 🔍 Troubleshooting

### Error: "Something went wrong"

1. Go to **Web** tab → **Error log**
2. Look for Python errors
3. Common issues:
   - Wrong path in WSGI file
   - Virtual environment not activated
   - Missing dependencies

### Error: Static files not loading

1. Check static files mapping in **Web** tab
2. Run `python manage.py collectstatic` again
3. Reload web app

### Error: Database errors

```bash
cd ~/SoftProject_api
source venv/bin/activate
python manage.py migrate
python manage.py init_services
```

### Error: Import errors

```bash
cd ~/SoftProject_api
source venv/bin/activate
pip install -r requirements.txt
```

### Can't access the site

1. Make sure you clicked "Reload" in Web tab
2. Check your username in URLs
3. Check error log
4. Try accessing: `https://your-username.pythonanywhere.com/api/services/`

---

## 🔧 Update Your Code Later

### If using GitHub:

```bash
# On PythonAnywhere Bash console
cd ~/SoftProject_api
source venv/bin/activate
git pull origin main
python manage.py migrate  # If models changed
python manage.py collectstatic --noinput  # If static files changed

# Go to Web tab and click Reload
```

### If uploading manually:

1. Upload changed files via **Files** tab
2. Go to **Web** tab
3. Click **Reload**

---

## 📱 Test Complete Flow

Once deployed, test everything:

### 1. Visit Frontend
```
https://your-username.pythonanywhere.com/
```

### 2. Create Account
- Click "Sign Up"
- Enter details
- Should redirect to dashboard

### 3. Test Services
- Services should load automatically
- Try cost calculator

### 4. Create Order
- Fill in order form
- Click "Place Order"
- Should see success message

### 5. View Orders
- Scroll down to "My Orders"
- Should see your order

---

## ⚙️ Important Configuration Notes

### Update ALLOWED_HOSTS

Edit `softproject_api/settings_production.py`:

```python
ALLOWED_HOSTS = ['your-username.pythonanywhere.com']
```

### Update CORS Origins

```python
CORS_ALLOWED_ORIGINS = [
    'https://your-username.pythonanywhere.com',
]
```

### Secure SECRET_KEY

Generate a new secret key:

```python
# In Python console on PythonAnywhere:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the output and update `SECRET_KEY` in `settings_production.py`.

---

## 🔒 Security Checklist (Before Going Live)

- [ ] Change `SECRET_KEY` to a random value
- [ ] Set `DEBUG = False` in production settings
- [ ] Update `ALLOWED_HOSTS` with your domain only
- [ ] Remove `/api/debug/users/` endpoint (comment out in `api/urls.py`)
- [ ] Enable password validation in settings
- [ ] Review CORS settings
- [ ] Set `CORS_ALLOW_ALL_ORIGINS = False`
- [ ] Add proper password requirements

---

## 📊 Free Tier Limitations

PythonAnywhere free tier includes:

- ✅ One web app at your-username.pythonanywhere.com
- ✅ 512 MB disk space
- ✅ SQLite database
- ✅ 100 seconds CPU time per day
- ❌ No HTTPS for custom domains (only pythonanywhere.com)
- ❌ No always-on tasks
- ❌ Limited to pythonanywhere.com subdomain

This is perfect for school projects and testing!

---

## 🎓 For Your School Project

Once deployed, you can share:

- **Frontend URL**: `https://your-username.pythonanywhere.com/`
- **API URL**: `https://your-username.pythonanywhere.com/api/`
- **API Docs**: Share the `API_DOCUMENTATION.md` file
- **Admin Panel**: `https://your-username.pythonanywhere.com/admin/`

---

## 📝 Quick Reference Commands

### Open Bash Console
```bash
cd ~/SoftProject_api
source venv/bin/activate
```

### Update Code (if using GitHub)
```bash
git pull origin main
python manage.py migrate
python manage.py collectstatic --noinput
# Then reload web app
```

### View Logs
```bash
tail -f /var/log/your-username.pythonanywhere.com.error.log
```

### Database Management
```bash
python manage.py shell
python manage.py dbshell
```

### Create Test User
```bash
python manage.py shell -c "
from api.models import User
User.objects.create_user(
    username='testuser',
    mobile_number='0771234567',
    password='test123'
)
"
```

---

## 🎉 Success Checklist

Once everything works:

- [ ] Frontend loads at your URL
- [ ] Can create new account
- [ ] Can sign in
- [ ] Services display correctly
- [ ] Cost calculator works
- [ ] Can create orders
- [ ] Orders display in list
- [ ] API endpoints respond correctly
- [ ] Admin panel accessible

---

## 🆘 Need Help?

1. **Check Error Logs**: Web tab → Error log
2. **Check Console Output**: When running commands
3. **PythonAnywhere Forums**: [https://www.pythonanywhere.com/forums/](https://www.pythonanywhere.com/forums/)
4. **PythonAnywhere Help**: [https://help.pythonanywhere.com/](https://help.pythonanywhere.com/)

---

## 📚 Additional Resources

- [PythonAnywhere Django Tutorial](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [PythonAnywhere Debugging](https://help.pythonanywhere.com/pages/DebuggingImportError/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)

---

**Good luck with your deployment! 🚀**

Your project should now be live and accessible from anywhere in the world!

Share the link with your classmates and professor: `https://your-username.pythonanywhere.com/`

