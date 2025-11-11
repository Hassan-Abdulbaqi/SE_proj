# SoftProject API Frontend

A modern, responsive web application for testing and interacting with the SoftProject API.

## Features

- 🔐 **User Authentication** - Sign up, sign in, and manage sessions
- 📦 **Service Catalog** - Browse available services (Electricity, Water, Gas)
- 💰 **Cost Calculator** - Calculate costs in Iraqi Dinar (IQD)
- 🛒 **Order Management** - Create and track orders
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🎨 **Modern UI** - Clean, intuitive interface with smooth animations

## Technology Stack

- **Pure JavaScript** (ES6+) - No build tools required
- **Modern CSS** - CSS Grid, Flexbox, CSS Variables
- **Fetch API** - For backend communication
- **Session-based Auth** - Secure authentication flow

## Getting Started

### Prerequisites

Make sure the Django backend is running:

```bash
cd ..
python manage.py runserver
```

The backend will run on `http://127.0.0.1:8000`

### Accessing the Frontend

The frontend is automatically served by Django. Simply visit:

```
http://127.0.0.1:8000/
```

Or open the HTML file directly in your browser (recommended for development):

```
file:///path/to/frontend/index.html
```

**Note:** When opening directly in a browser, you may need to enable CORS. The Django backend is already configured to allow cross-origin requests from anywhere in development mode.

## Usage Guide

### 1. Authentication

**Sign Up:**
- Enter username, mobile number, password, and optional email
- Click "Sign Up" to create your account
- You'll be automatically logged in

**Sign In:**
- Enter your mobile number and password
- Click "Sign In" to access your dashboard

### 2. Browse Services

After logging in, you'll see available services:
- ⚡ Electricity (كهرباء) - 200 IQD per kWh
- 💧 Water (ماء) - 200 IQD per Liter
- 🔥 Gas (غاز) - 200 IQD per m³

### 3. Calculate Costs

Use the cost calculator to estimate expenses:
1. Select a service
2. Enter quantity
3. Click "Calculate Cost"
4. View the breakdown with total in IQD

### 4. Place Orders

To create an order:
1. Select a service
2. Enter quantity
3. Provide delivery location
4. Choose payment method (cash or card)
5. Set delivery cost and estimated time
6. Add optional notes
7. Click "Place Order"

### 5. Track Orders

View all your orders at the bottom of the dashboard:
- Order ID and status
- Service details and quantity
- Location and payment method
- Cost breakdown (service + delivery)
- Order timestamps

## File Structure

```
frontend/
├── index.html      # Main HTML structure
├── app.js          # JavaScript application logic
├── styles.css      # Modern CSS styling
└── README.md       # This file
```

## API Configuration

The frontend is configured to connect to:

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

If your backend runs on a different URL, update this constant in `app.js`.

## Features in Detail

### State Management
- Client-side state management for user, services, and orders
- Automatic session persistence via cookies
- Auto-login on page refresh if session exists

### UI Components
- Toast notifications for user feedback
- Status badges for order tracking
- Responsive card layouts
- Modern form designs with validation

### API Integration
- Automatic CSRF handling (disabled for dev mode)
- Session-based authentication
- Error handling and user feedback
- Proper HTTP method usage (GET, POST, PUT, DELETE)

## Browser Compatibility

Tested and working on:
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

Requires a modern browser with ES6+ support.

## Development Mode

The backend is configured for development with:
- ✅ CORS enabled for all origins
- ✅ CSRF checks disabled
- ✅ Password validation disabled
- ✅ Debug mode enabled

**⚠️ WARNING:** These settings are UNSAFE for production!

## Troubleshooting

### Issue: "Authentication credentials were not provided"
- **Solution:** Sign in again. Your session may have expired.

### Issue: "Service not found"
- **Solution:** Run `python manage.py init_services` to populate the database.

### Issue: CORS errors when opening HTML directly
- **Solution:** Access via Django at `http://127.0.0.1:8000/` or use a local web server.

### Issue: Styles not loading
- **Solution:** Ensure `styles.css` and `app.js` are in the same directory as `index.html`.

## Currency Information

All prices and calculations are in **Iraqi Dinar (IQD)**:
- Symbol: IQD or د.ع
- Format: 20,000.00 IQD
- The API returns decimal values with 2 decimal places

## Next Steps

To extend this frontend:
1. Add order tracking with real-time updates
2. Implement profile editing
3. Add password change functionality
4. Create an admin dashboard
5. Add filtering and sorting for orders
6. Implement pagination for large datasets

## License

This is a school project for educational purposes.

