# PythonAnywhere Deployment Checklist ✅

Quick reference checklist for deploying to PythonAnywhere.

---

## Pre-Deployment

- [ ] All code is working locally
- [ ] Tested authentication (signup/signin)
- [ ] Tested services and orders
- [ ] Services initialized (`python manage.py init_services`)
- [ ] Requirements.txt is up to date

---

## PythonAnywhere Setup

### 1. Account & Project Upload
- [ ] Created PythonAnywhere account
- [ ] Uploaded/cloned project to `~/SoftProject_api/`
- [ ] All files are present (manage.py, api/, frontend/, etc.)

### 2. Virtual Environment
- [ ] Created venv: `python3.10 -m venv venv`
- [ ] Activated: `source venv/bin/activate`
- [ ] Installed dependencies: `pip install -r requirements.txt`

### 3. Database Setup
- [ ] Ran migrations: `python manage.py migrate`
- [ ] Initialized services: `python manage.py init_services`
- [ ] Created superuser: `python manage.py createsuperuser`
- [ ] Collected static files: `python manage.py collectstatic --noinput`

### 4. Web App Configuration
- [ ] Created new web app (Manual configuration, Python 3.10)
- [ ] Set virtualenv path: `/home/YOUR_USERNAME/SoftProject_api/venv`
- [ ] Updated WSGI file with correct paths
- [ ] Replaced `YOUR_USERNAME` in WSGI file
- [ ] Added static files mapping: `/static/` → `/home/YOUR_USERNAME/SoftProject_api/staticfiles/`
- [ ] Added frontend mapping: `/frontend/` → `/home/YOUR_USERNAME/SoftProject_api/frontend/`

### 5. Settings Configuration
- [ ] Created `settings_production.py`
- [ ] Updated `ALLOWED_HOSTS` with your domain
- [ ] Updated `CORS_ALLOWED_ORIGINS`
- [ ] Changed `SECRET_KEY` to new random value
- [ ] Set appropriate `DEBUG` value
- [ ] Configured database path

### 6. First Deployment
- [ ] Clicked "Reload" on Web tab
- [ ] No errors in error log
- [ ] Can access homepage: `https://your-username.pythonanywhere.com/`
- [ ] Can access API: `https://your-username.pythonanywhere.com/api/services/`

---

## Testing After Deployment

### Frontend Tests
- [ ] Homepage loads correctly
- [ ] Sign up form works
- [ ] Sign in form works
- [ ] Services display properly
- [ ] Cost calculator works
- [ ] Order creation works
- [ ] Orders list displays
- [ ] Logout works

### API Tests
- [ ] GET `/api/services/` returns data
- [ ] GET `/api/services/calculate_cost/?service_id=1&quantity=100` works
- [ ] POST `/api/auth/signup/` creates user
- [ ] POST `/api/auth/signin/` logs in
- [ ] GET `/api/profile/` returns user (when logged in)
- [ ] POST `/api/orders/checkout/` creates order (when logged in)
- [ ] GET `/api/orders/` lists orders (when logged in)

### Admin Panel
- [ ] Can access: `https://your-username.pythonanywhere.com/admin/`
- [ ] Can log in with superuser credentials
- [ ] Can view users
- [ ] Can view orders
- [ ] Can view services

---

## Common Issues & Fixes

### ❌ "Something went wrong"
- [ ] Checked error log in Web tab
- [ ] Verified WSGI file paths
- [ ] Verified virtualenv path
- [ ] Tried reloading web app

### ❌ Static files not loading
- [ ] Ran `python manage.py collectstatic --noinput`
- [ ] Verified static files mapping
- [ ] Reloaded web app

### ❌ Database errors
- [ ] Ran `python manage.py migrate`
- [ ] Ran `python manage.py init_services`
- [ ] Verified db.sqlite3 file exists

### ❌ Import errors
- [ ] Activated virtual environment
- [ ] Ran `pip install -r requirements.txt`
- [ ] Checked sys.path in WSGI file

### ❌ 404 on pages
- [ ] Checked ALLOWED_HOSTS in settings
- [ ] Verified URL patterns in urls.py
- [ ] Checked frontend files mapping

---

## Final Polish

### Before Sharing with Professor
- [ ] Tested all features end-to-end
- [ ] Created test account to demonstrate
- [ ] Verified all services are initialized
- [ ] Created sample orders
- [ ] Admin panel accessible
- [ ] No errors in error log
- [ ] All pages load quickly

### Documentation Ready
- [ ] README.md is updated
- [ ] API_DOCUMENTATION.md is complete
- [ ] Have deployment URL ready
- [ ] Have admin credentials noted (for demo)

---

## URLs to Share

Write down your URLs:

- **Main Site**: https://________________.pythonanywhere.com/
- **API Root**: https://________________.pythonanywhere.com/api/
- **Services**: https://________________.pythonanywhere.com/api/services/
- **Admin**: https://________________.pythonanywhere.com/admin/

---

## Credentials for Demo

**Admin Account:**
- Username: _______________
- Password: _______________

**Test User:**
- Mobile: _______________
- Password: _______________

---

## Quick Commands Reference

### Access Project
```bash
cd ~/SoftProject_api
source venv/bin/activate
```

### Update Code (if using Git)
```bash
git pull origin main
python manage.py migrate
python manage.py collectstatic --noinput
# Then reload web app in Web tab
```

### Check Logs
```bash
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

### Django Shell
```bash
python manage.py shell
```

### Create Test Data
```bash
python manage.py init_services
```

---

## Maintenance Schedule

- [ ] Check error logs weekly
- [ ] Update code when needed
- [ ] Monitor disk space usage
- [ ] Test all features periodically

---

## Presentation Day

- [ ] Site is up and running
- [ ] Have backup of project locally
- [ ] Know admin credentials
- [ ] Tested on mobile devices
- [ ] Prepared demo flow:
  1. Show homepage
  2. Create new account
  3. Browse services
  4. Calculate cost
  5. Create order
  6. Show order history
  7. Show admin panel

---

## Emergency Contacts

- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **Forums**: https://www.pythonanywhere.com/forums/
- **Your GitHub**: https://github.com/YOUR_USERNAME/SoftProject_api

---

**Status**: 
- [ ] Local development ✓
- [ ] Deployed to PythonAnywhere
- [ ] Tested and working
- [ ] Ready for presentation

**Deployment Date**: _______________

**Last Updated**: _______________

---

🎓 **For SE Class**  
📧 Professor can access: https://YOUR_USERNAME.pythonanywhere.com/

