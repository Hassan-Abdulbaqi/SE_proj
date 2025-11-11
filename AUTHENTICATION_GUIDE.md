# Authentication Guide & Troubleshooting

## 🔍 Current Issue Diagnosed

Based on the debug logs, the issue is **NOT a code problem** - it's a **data mismatch**:

### What's Happening:
```
[DEBUG] Signin request data: {'mobile_number': '0772906728', 'password': '123'}
[DEBUG] Signin validation errors: {'non_field_errors': [ErrorDetail(string='Invalid credentials', code='invalid')]}
```

### Why It's Failing:
- **Mobile number in database**: `07722906728` (notice the extra '2' after '077')
- **Mobile number entered**: `0772906728` (missing that '2')
- **Result**: User not found → "Invalid credentials"

## ✅ Latest Fixes Applied

### 1. **Better Error Messages**
   - Now tells you specifically if mobile number doesn't exist
   - Shows separate error for wrong password
   - File: `api/serializers.py`

### 2. **Custom Authentication Backend**
   - Added `MobileNumberBackend` for mobile-based auth
   - File: `api/backends.py` (NEW)
   - Configured in: `softproject_api/settings.py`

### 3. **Frontend Error Handling**
   - Now displays field-specific errors
   - Shows exact error message from backend
   - File: `frontend/app.js`

### 4. **Debug Endpoint (Development Only)**
   - New endpoint: `GET /api/debug/users/`
   - Lists all existing users and their mobile numbers
   - Helps identify what accounts exist
   - **⚠️ NEVER use in production!**

## 📱 How to Use the Debug Endpoint

### Option 1: Browser
Visit: `http://127.0.0.1:8000/api/debug/users/`

### Option 2: Terminal
```bash
curl http://127.0.0.1:8000/api/debug/users/
```

### Expected Response:
```json
{
  "total_users": 1,
  "users": [
    {
      "id": 1,
      "username": "Hassan",
      "mobile_number": "07722906728",
      "email": ""
    }
  ],
  "warning": "This endpoint should NEVER be used in production!"
}
```

## 🔧 Solution Options

### Option 1: Sign In with Correct Mobile Number
Use the EXACT mobile number from the database:
- **Correct**: `07722906728`
- **Incorrect**: `0772906728`

### Option 2: Create New Account
Sign up with a new mobile number:
1. Go to `http://127.0.0.1:8000/`
2. Fill in the Sign Up form:
   - Username: `testuser` (or any name)
   - Mobile Number: `0772906728` (or any number)
   - Password: `123` (or any password - no validation!)
   - Confirm Password: `123`
   - Email: (optional)
3. Click "Create Account"

### Option 3: Delete Existing User (Fresh Start)
```bash
python manage.py shell -c "from api.models import User; User.objects.filter(mobile_number='07722906728').delete(); print('User deleted')"
```

## 🧪 Testing Steps

### 1. Check Existing Users
```bash
# Visit debug endpoint
curl http://127.0.0.1:8000/api/debug/users/
```

### 2. Sign Up (Create New Account)
1. Go to `http://127.0.0.1:8000/`
2. Fill in the **Sign Up** form (left side)
3. Use a NEW mobile number (e.g., `0771234567`)
4. Use simple password (e.g., `123`)
5. Click "Create Account"
6. You should see: ✅ "Account created successfully!"

### 3. Sign In (Use Existing Account)
1. Fill in the **Sign In** form (right side)
2. Enter EXACT mobile number from database
3. Enter the correct password
4. Click "Sign In"
5. You should see: ✅ "Signed in successfully!"

### 4. Watch Server Console
The server will now show helpful debug messages:
```bash
[DEBUG] Signup request data: {'username': 'testuser', ...}
[DEBUG] Signin request data: {'mobile_number': '0771234567', ...}
```

If there are errors:
```bash
[DEBUG] Signin validation errors: {
    'mobile_number': ['No account found with mobile number 0771234567. Please sign up first.']
}
```
OR
```bash
[DEBUG] Signin validation errors: {
    'password': ['Incorrect password. Please try again.']
}
```

## 🎯 New Error Messages

The system now provides helpful, specific errors:

### Mobile Number Not Found:
```
No account found with mobile number 0772906728. Please sign up first.
```

### Wrong Password:
```
Incorrect password. Please try again.
```

### Account Disabled:
```
This account has been disabled.
```

## 🔄 Restart Required

After applying these changes, restart the Django server:

```bash
# Press Ctrl+C to stop current server
python manage.py runserver
```

## 📋 Quick Reference

### Debug Endpoint
- **URL**: `http://127.0.0.1:8000/api/debug/users/`
- **Method**: GET
- **Auth**: None required
- **Purpose**: See all existing users

### Sign Up Endpoint
- **URL**: `http://127.0.0.1:8000/api/auth/signup/`
- **Method**: POST
- **Body**: `{username, mobile_number, password, password_confirm, email?}`

### Sign In Endpoint
- **URL**: `http://127.0.0.1:8000/api/auth/signin/`
- **Method**: POST
- **Body**: `{mobile_number, password}`

## 🎯 Expected Behavior NOW

### Signing In with Wrong Mobile Number:
❌ **Old**: "Invalid credentials" (vague)
✅ **New**: "No account found with mobile number 0772906728. Please sign up first."

### Signing In with Wrong Password:
❌ **Old**: "Invalid credentials" (vague)
✅ **New**: "Incorrect password. Please try again."

### Frontend Display:
- Error message shown as **red toast notification**
- Specific field errors highlighted
- Clear, actionable feedback

## 🔒 Files Changed

1. **`api/backends.py`** (NEW) - Custom mobile number authentication
2. **`api/serializers.py`** - Better error messages
3. **`api/views.py`** - Debug endpoint + existing debug logs
4. **`api/urls.py`** - Added debug endpoint route
5. **`frontend/app.js`** - Better error display
6. **`softproject_api/settings.py`** - Added authentication backends

## ⚠️ Important Notes

1. **Debug endpoint is for DEVELOPMENT ONLY**
   - It exposes all user data
   - Never deploy with this enabled
   - Automatically disabled when `DEBUG=False`

2. **No Password Validation**
   - Any password works (even "123")
   - This is intentional for development
   - Change in production!

3. **Mobile Number Format**
   - No validation on format
   - Exact match required for login
   - Be consistent (e.g., always include or exclude spaces)

## 🚀 Next Steps

1. **Restart the server** (if not done already)
2. **Check existing users**: Visit `/api/debug/users/`
3. **Create new test account** OR **sign in with existing account**
4. **Monitor server console** for debug output
5. **Report any new errors** with the debug output

The authentication should now work perfectly with clear, helpful error messages! 🎉

