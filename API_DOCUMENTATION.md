# SoftProject API Documentation

## Overview

A comprehensive REST API for utility services (Electricity, Water, Gas) ordering system with support for user authentication, service management, cost calculation, and order tracking.

**Version**: 1.0  
**Live URL**: `https://sh3ewit.pythonanywhere.com/`  
**API Base URL**: `https://sh3ewit.pythonanywhere.com/api/`  
**Local Dev URL**: `http://127.0.0.1:8000/api/`  
**Currency**: Iraqi Dinar (IQD) 🇮🇶  
**Authentication**: Session-based (cookies)

---

## 🚀 Quick Start

### 🌐 Live Deployment

- **Frontend Web App**: `https://sh3ewit.pythonanywhere.com/`
- **API Endpoints**: `https://sh3ewit.pythonanywhere.com/api/`
- **Django Admin**: `https://sh3ewit.pythonanywhere.com/admin/`
- **Services API**: `https://sh3ewit.pythonanywhere.com/api/services/`

### 💻 Local Development

- **Frontend Web App**: `http://127.0.0.1:8000/`
- **API Endpoints**: `http://127.0.0.1:8000/api/`
- **Django Admin**: `http://127.0.0.1:8000/admin/`
- **Debug Users** (Dev only): `http://127.0.0.1:8000/api/debug/users/`

### Quick Test Flow

1. **Create Account**: POST `/api/auth/signup/`
2. **Sign In**: POST `/api/auth/signin/`
3. **Browse Services**: GET `/api/services/`
4. **Calculate Cost**: GET `/api/services/calculate_cost/?service_id=1&quantity=100`
5. **Create Order**: POST `/api/orders/checkout/`
6. **View Orders**: GET `/api/orders/`

---

## 🔐 Authentication

All authentication uses **mobile number** instead of username.

### Sign Up

Create a new user account.

**Endpoint**: `POST /api/auth/signup/`  
**Authentication**: None required  
**Content-Type**: `application/json`

**Request Body**:
```json
{
  "username": "john_doe",
  "mobile_number": "0771234567",
  "password": "mypassword123",
  "password_confirm": "mypassword123",
  "email": "john@example.com"
}
```

**Field Requirements**:
- `username` (required): Unique username
- `mobile_number` (required): Unique mobile number (any format)
- `password` (required): Any password (no validation in dev mode)
- `password_confirm` (required): Must match password
- `email` (optional): Email address

**Success Response (201 Created)**:
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "mobile_number": "0771234567",
    "email": "john@example.com",
    "first_name": "",
    "last_name": ""
  }
}
```

**Error Responses**:

```json
// Passwords don't match
{
  "password": "Passwords don't match"
}

// Username already exists
{
  "username": ["A user with that username already exists."]
}

// Mobile number already exists
{
  "mobile_number": ["User with this mobile number already exists."]
}
```

---

### Sign In

Authenticate with mobile number and password.

**Endpoint**: `POST /api/auth/signin/`  
**Authentication**: None required  
**Content-Type**: `application/json`

**Request Body**:
```json
{
  "mobile_number": "0771234567",
  "password": "mypassword123"
}
```

**Success Response (200 OK)**:
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "mobile_number": "0771234567",
    "email": "john@example.com",
    "first_name": "",
    "last_name": ""
  }
}
```

**Error Responses**:

```json
// User not found
{
  "error": "No account found with mobile number 0771234567. Please sign up first."
}

// Wrong password
{
  "error": "Incorrect password. Please try again."
}

// Account disabled
{
  "error": "This account has been disabled"
}

// Missing fields
{
  "error": "Mobile number and password are required"
}
```

---

### Sign Out

Log out the current user.

**Endpoint**: `POST /api/auth/signout/`  
**Authentication**: Required (session cookie)

**Success Response (200 OK)**:
```json
{
  "message": "Logout successful"
}
```

---

### Get CSRF Token (Deprecated)

CSRF protection is disabled in development mode.

**Endpoint**: `GET /api/auth/csrf/`  
**Authentication**: None required

**Response (200 OK)**:
```json
{
  "csrfToken": null,
  "message": "CSRF checks are disabled in development mode."
}
```

---

### Debug: List Users (Development Only)

⚠️ **WARNING**: This endpoint exposes all user data. NEVER use in production!

**Endpoint**: `GET /api/debug/users/`  
**Authentication**: None required (dev only)

**Response (200 OK)**:
```json
{
  "total_users": 2,
  "users": [
    {
      "id": 1,
      "username": "john_doe",
      "mobile_number": "0771234567",
      "email": "john@example.com"
    },
    {
      "id": 2,
      "username": "jane_smith",
      "mobile_number": "0772345678",
      "email": "jane@example.com"
    }
  ],
  "warning": "This endpoint should NEVER be used in production!"
}
```

---

## 👤 Profile Management

### Get Profile

Retrieve the authenticated user's profile.

**Endpoint**: `GET /api/profile/`  
**Authentication**: Required

**Response (200 OK)**:
```json
{
  "id": 1,
  "username": "john_doe",
  "mobile_number": "0771234567",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

### Update Profile

Update user profile information.

**Endpoint**: `PUT /api/profile/update/` or `PATCH /api/profile/update/`  
**Authentication**: Required  
**Content-Type**: `application/json`

**Request Body** (all fields optional):
```json
{
  "username": "new_username",
  "mobile_number": "0779876543",
  "email": "newemail@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Success Response (200 OK)**:
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "new_username",
    "mobile_number": "0779876543",
    "email": "newemail@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

---

### Change Password

Change the user's password.

**Endpoint**: `POST /api/profile/change-password/`  
**Authentication**: Required  
**Content-Type**: `application/json`

**Request Body**:
```json
{
  "old_password": "current_password",
  "new_password": "new_password"
}
```

**Success Response (200 OK)**:
```json
{
  "message": "Password changed successfully"
}
```

**Error Response**:
```json
{
  "error": "Invalid old password"
}
```

---

## 📦 Services

Available utility services with pricing in IQD.

### List All Services

Retrieve all available services.

**Endpoint**: `GET /api/services/`  
**Authentication**: None required

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "service_type": "electricity",
    "name_ar": "كهرباء",
    "name_en": "Electricity",
    "price_per_unit": "200.00",
    "unit_name": "kWh",
    "unit_name_ar": "كيلوواط ساعة",
    "currency": "IQD"
  },
  {
    "id": 2,
    "service_type": "water",
    "name_ar": "ماء",
    "name_en": "Water",
    "price_per_unit": "200.00",
    "unit_name": "Liter",
    "unit_name_ar": "لتر",
    "currency": "IQD"
  },
  {
    "id": 3,
    "service_type": "gas",
    "name_ar": "غاز",
    "name_en": "Gas",
    "price_per_unit": "200.00",
    "unit_name": "m³",
    "unit_name_ar": "متر مكعب",
    "currency": "IQD"
  }
]
```

---

### Get Service Details

Retrieve details of a specific service.

**Endpoint**: `GET /api/services/{id}/`  
**Authentication**: None required

**Example**: `GET /api/services/1/`

**Response (200 OK)**:
```json
{
  "id": 1,
  "service_type": "electricity",
  "name_ar": "كهرباء",
  "name_en": "Electricity",
  "price_per_unit": "200.00",
  "unit_name": "kWh",
  "unit_name_ar": "كيلوواط ساعة",
  "currency": "IQD"
}
```

**Error Response (404 Not Found)**:
```json
{
  "detail": "Not found."
}
```

---

### Calculate Cost

Calculate the total cost for a service based on quantity.

**Endpoint**: `GET /api/services/calculate_cost/`  
**Authentication**: None required

**Query Parameters**:
- `service_id` (required): Service ID (1, 2, or 3)
- `quantity` (required): Number of units (decimal allowed)

**Example**: `GET /api/services/calculate_cost/?service_id=1&quantity=150.5`

**Response (200 OK)**:
```json
{
  "service": {
    "id": 1,
    "service_type": "electricity",
    "name_ar": "كهرباء",
    "name_en": "Electricity",
    "price_per_unit": "200.00",
    "unit_name": "kWh",
    "unit_name_ar": "كيلوواط ساعة",
    "currency": "IQD"
  },
  "quantity": "150.50",
  "cost": "30100.00",
  "currency": "IQD"
}
```

**Error Responses**:

```json
// Missing parameters
{
  "error": "service_id and quantity are required"
}

// Service not found
{
  "error": "Service not found"
}

// Invalid quantity
{
  "error": "Invalid quantity"
}
```

---

## 🛒 Orders

Manage service orders.

### List User Orders

Retrieve all orders for the authenticated user.

**Endpoint**: `GET /api/orders/`  
**Authentication**: Required

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "john_doe",
      "mobile_number": "0771234567",
      "email": "john@example.com",
      "first_name": "",
      "last_name": ""
    },
    "service": {
      "id": 1,
      "service_type": "electricity",
      "name_ar": "كهرباء",
      "name_en": "Electricity",
      "price_per_unit": "200.00",
      "unit_name": "kWh",
      "unit_name_ar": "كيلوواط ساعة",
      "currency": "IQD"
    },
    "service_id": 1,
    "quantity": "150.00",
    "service_cost": "30000.00",
    "delivery_cost": "5000.00",
    "total_cost": "35000.00",
    "location": "Baghdad, Al-Mansour District",
    "payment_method": "cash",
    "currency": "IQD",
    "notes": "Please deliver between 9 AM and 5 PM",
    "status": "pending",
    "estimated_delivery_time": 60,
    "created_at": "2025-11-11T19:00:00Z",
    "updated_at": "2025-11-11T19:00:00Z"
  }
]
```

---

### Get Order Details

Retrieve details of a specific order.

**Endpoint**: `GET /api/orders/{id}/`  
**Authentication**: Required (must be order owner)

**Example**: `GET /api/orders/1/`

**Response (200 OK)**: Same structure as order in list above

**Error Response (404 Not Found)**:
```json
{
  "detail": "Not found."
}
```

---

### Create Order (Checkout)

Create a new service order.

**Endpoint**: `POST /api/orders/checkout/`  
**Authentication**: Required  
**Content-Type**: `application/json`

**Request Body**:
```json
{
  "service_id": 1,
  "quantity": 150,
  "location": "Baghdad, Al-Mansour District, Street 14",
  "payment_method": "cash",
  "delivery_cost": 5000,
  "estimated_delivery_time": 60,
  "notes": "Please deliver between 9 AM and 5 PM"
}
```

**Field Requirements**:
- `service_id` (required, integer): Service ID (1, 2, or 3)
- `quantity` (required, decimal): Number of units (min: 0.01)
- `location` (required, string): Delivery address
- `payment_method` (required, enum): "cash" or "card"
- `delivery_cost` (optional, decimal): Delivery fee in IQD (default: 0)
- `estimated_delivery_time` (optional, integer): Minutes (default: 60)
- `notes` (optional, string): Special instructions

**Success Response (201 Created)**:
```json
{
  "message": "Order created successfully",
  "order": {
    "id": 1,
    "user": { ... },
    "service": { ... },
    "service_id": 1,
    "quantity": "150.00",
    "service_cost": "30000.00",
    "delivery_cost": "5000.00",
    "total_cost": "35000.00",
    "location": "Baghdad, Al-Mansour District, Street 14",
    "payment_method": "cash",
    "currency": "IQD",
    "notes": "Please deliver between 9 AM and 5 PM",
    "status": "pending",
    "estimated_delivery_time": 60,
    "created_at": "2025-11-11T19:00:00Z",
    "updated_at": "2025-11-11T19:00:00Z"
  }
}
```

**Error Responses**:

```json
// Service not found
{
  "error": "Service not found"
}

// Invalid quantity
{
  "quantity": ["Ensure this value is greater than or equal to 0.01."]
}

// Invalid payment method
{
  "payment_method": ["\"bitcoin\" is not a valid choice."]
}
```

---

### Track Order

Get tracking information for a specific order.

**Endpoint**: `GET /api/orders/{id}/track/`  
**Authentication**: Required (must be order owner)

**Example**: `GET /api/orders/1/track/`

**Response (200 OK)**:
```json
{
  "id": 1,
  "order": {
    "id": 1,
    "user": { ... },
    "service": { ... },
    "quantity": "150.00",
    "service_cost": "30000.00",
    "delivery_cost": "5000.00",
    "total_cost": "35000.00",
    "location": "Baghdad, Al-Mansour District",
    "payment_method": "cash",
    "currency": "IQD",
    "notes": "Please deliver between 9 AM and 5 PM",
    "status": "in_progress",
    "estimated_delivery_time": 60,
    "created_at": "2025-11-11T19:00:00Z",
    "updated_at": "2025-11-11T19:15:00Z"
  },
  "remaining_delivery_time": 45,
  "last_updated": "2025-11-11T19:15:00Z"
}
```

---

## 📊 Data Models

### Order Status Values

- `pending` - Order placed, awaiting confirmation
- `confirmed` - Order confirmed by provider
- `in_progress` - Service delivery in progress
- `delivered` - Order completed successfully
- `cancelled` - Order cancelled

### Payment Methods

- `cash` - Cash on delivery
- `card` - Card payment (online or on delivery)

### Service Types

- `electricity` - Electrical power (kWh)
- `water` - Water supply (Liters)
- `gas` - Natural gas (m³)

---

## 💰 Pricing Information

All prices are in **Iraqi Dinar (IQD)**.

### Current Rates (Default)

| Service | Price per Unit | Unit |
|---------|---------------|------|
| Electricity | 200.00 IQD | kWh |
| Water | 200.00 IQD | Liter |
| Gas | 200.00 IQD | m³ |

### Cost Calculation Formula

```
service_cost = price_per_unit × quantity
total_cost = service_cost + delivery_cost
```

**Example**:
- Service: Electricity (200 IQD/kWh)
- Quantity: 150 kWh
- Delivery: 5,000 IQD
- **Total**: (200 × 150) + 5,000 = **35,000 IQD**

---

## 🔧 Error Handling

### Standard Error Format

```json
{
  "error": "Error message here"
}
```

### HTTP Status Codes

- `200 OK` - Request succeeded
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Common Error Responses

**Authentication Required (401)**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Permission Denied (403)**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**Not Found (404)**:
```json
{
  "detail": "Not found."
}
```

**Validation Error (400)**:
```json
{
  "field_name": ["Error message for this field"]
}
```

---

## 🔒 Development Mode Configuration

⚠️ **This API is configured for development with ALL security restrictions removed:**

### Security Settings (UNSAFE for Production)

- ✅ **CORS**: Enabled for all origins
- ✅ **CSRF**: Protection completely disabled
- ✅ **Password Validation**: Disabled (any password works)
- ✅ **Host Validation**: All hosts allowed
- ✅ **Debug Mode**: Enabled
- ✅ **Session Authentication**: Without CSRF checks

### Development-Only Endpoints

- `/api/debug/users/` - Lists all users (⚠️ NEVER use in production!)

### Important Notes

1. **Passwords**: No validation - "123" is a valid password
2. **Mobile Numbers**: No format validation - any string works
3. **Email**: Optional and not validated
4. **Sessions**: Stored in cookies, persist across requests
5. **Error Messages**: Verbose for debugging

**⚠️ WARNING**: This configuration is EXTREMELY UNSAFE for production. Always implement proper security before deploying!

---

## 🧪 Testing with cURL

**Note**: Replace `https://sh3ewit.pythonanywhere.com` with `http://127.0.0.1:8000` for local testing.

### Sign Up
```bash
# Production
curl -X POST https://sh3ewit.pythonanywhere.com/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "mobile_number": "0771234567",
    "password": "test123",
    "password_confirm": "test123"
  }'

# Local
curl -X POST http://127.0.0.1:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "mobile_number": "0771234567",
    "password": "test123",
    "password_confirm": "test123"
  }'
```

### Sign In
```bash
# Production
curl -X POST https://sh3ewit.pythonanywhere.com/api/auth/signin/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "mobile_number": "0771234567",
    "password": "test123"
  }'
```

### List Services
```bash
# Production
curl https://sh3ewit.pythonanywhere.com/api/services/

# Local
curl http://127.0.0.1:8000/api/services/
```

### Calculate Cost
```bash
# Production
curl "https://sh3ewit.pythonanywhere.com/api/services/calculate_cost/?service_id=1&quantity=100"

# Local
curl "http://127.0.0.1:8000/api/services/calculate_cost/?service_id=1&quantity=100"
```

### Create Order (requires authentication)
```bash
# Production
curl -X POST https://sh3ewit.pythonanywhere.com/api/orders/checkout/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "service_id": 1,
    "quantity": 100,
    "location": "Baghdad, Iraq",
    "payment_method": "cash",
    "delivery_cost": 5000,
    "estimated_delivery_time": 60
  }'
```

### List Orders (requires authentication)
```bash
# Production
curl https://sh3ewit.pythonanywhere.com/api/orders/ \
  -b cookies.txt
```

---

## 🎨 Frontend Web Interface

A modern, responsive web application is available at the root URL.

### Access
- **Live**: `https://sh3ewit.pythonanywhere.com/`
- **Local**: `http://127.0.0.1:8000/`

### Features
- 🔐 User authentication (Sign Up / Sign In)
- 📦 Browse services with visual cards
- 💰 Real-time cost calculator
- 🛒 Create and manage orders
- 📱 Fully responsive design
- 🎨 Modern UI with animations
- 🔔 Toast notifications

### Technologies
- **Pure JavaScript** (ES6+) - No build tools required
- **Modern CSS** - CSS Grid, Flexbox, Variables
- **Session-based Auth** - Automatic login persistence

See `frontend/README.md` for detailed documentation.

---

## 📚 Additional Resources

- **Main README**: `README.md` - Project setup and overview
- **Frontend Docs**: `frontend/README.md` - Frontend documentation
- **Authentication Guide**: `AUTHENTICATION_GUIDE.md` - Auth troubleshooting
- **Backend Fix**: `BACKEND_FIX.md` - Recent fixes applied

---

## 🤝 Support

This is a school/educational project. For issues:

1. Check the server console for debug output
2. Visit `/api/debug/users/` to see existing users
3. Review the authentication guide
4. Ensure services are initialized: `python manage.py init_services`

---

## 📝 Notes

- All monetary values use 2 decimal places
- Dates are in ISO 8601 format (UTC)
- Session cookies expire based on Django settings
- Orders are sorted by creation date (newest first)
- Mobile numbers must be unique per user
- Usernames must be unique per user

---

**Last Updated**: November 11, 2025  
**API Version**: 1.0  
**Django Version**: 4.2+  
**DRF Version**: 3.14+

**Live Deployment**: [https://sh3ewit.pythonanywhere.com/](https://sh3ewit.pythonanywhere.com/)

---

Made with ❤️ for SE class
