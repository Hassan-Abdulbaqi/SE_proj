# Frontend API Configuration

## Current Configuration

The frontend is currently configured to connect to:

**Production**: `https://sh3ewit.pythonanywhere.com/api`

## Switching Between Environments

### For Production (PythonAnywhere)

In `frontend/app.js`, line 4:
```javascript
const API_BASE_URL = 'https://sh3ewit.pythonanywhere.com/api';
```

### For Local Development

In `frontend/app.js`, line 4:
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

## Quick Switch

Just change this one line in `app.js` and refresh your browser:

```javascript
// For local development:
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// For production:
const API_BASE_URL = 'https://sh3ewit.pythonanywhere.com/api';
```

## Testing

After changing the API URL:
1. Save the file
2. Refresh your browser (Ctrl+F5 or Cmd+Shift+R for hard refresh)
3. Try signing in or creating an account
4. Check the browser console (F12) for any CORS or connection errors

## Notes

- Production uses HTTPS (secure)
- Local development uses HTTP
- Make sure your Django backend has the correct CORS settings for the environment you're using

