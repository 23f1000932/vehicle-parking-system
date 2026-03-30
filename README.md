# 🚗 Vehicle Parking Management System

A full-stack web application for managing parking lots, spots, and reservations. Built with Flask (Python) for the backend and Vue.js 3 for the frontend, featuring role-based access control, real-time spot availability, cost calculation, and analytics dashboards.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Database Schema](#-database-schema)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [Default Credentials](#-default-credentials)
- [Usage Guide](#-usage-guide)
- [Background Tasks](#-background-tasks)

---

## ✨ Features

### 👤 User Features
- **User Registration & Authentication** - Secure signup and login with token-based authentication
- **Browse Parking Lots** - View all available parking lots with real-time spot availability
- **Make Reservations** - Book a parking spot with automatic spot assignment
- **Reservation History** - View past and current reservations
- **Real-time Cost Calculation** - Calculate parking cost before checkout
- **End Reservation & Payment** - Complete parking session with simulated payment
- **Analytics Dashboard** - View reservation summary with interactive charts

### 🔐 Admin Features
- **Parking Lot Management** - Create, edit, and delete parking lots
- **Dynamic Spot Management** - Automatically manage spots when lot capacity changes
- **User Management** - View all registered users and their details
- **System Analytics** - Bar charts showing total vs occupied spots per lot
- **Reservation Overview** - System-wide reservation monitoring

### ⚡ System Features
- **Redis Caching** - 5-minute cache for parking lot data with automatic invalidation
- **Role-Based Access Control** - Separate workflows for Admin and User roles
- **Background Tasks** - Celery integration for email notifications and reports
- **Email Notifications** - Daily reminders and monthly activity reports
- **CORS Support** - Seamless frontend-backend communication
- **Responsive Design** - Bootstrap-powered UI for all screen sizes

---

## 🛠 Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.x | Core language |
| Flask | 3.1.1 | Web framework |
| SQLAlchemy | 2.0.41 | ORM for database operations |
| Flask-SQLAlchemy | 3.1.1 | Flask integration for SQLAlchemy |
| Flask-Security-Too | 5.6.2 | Authentication & authorization |
| Flask-Login | 0.6.3 | Session management |
| Flask-CORS | - | Cross-origin support |
| SQLite | 3 | Database |
| Redis | - | Caching & message broker |
| Celery | - | Background task queue |
| WTForms | 3.2.1 | Form validation |
| Bcrypt | - | Password hashing |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Vue.js | 3.5.13 | Frontend framework |
| Vite | 6.2.4 | Build tool & dev server |
| Vue Router | 4.5.0 | Client-side routing |
| Pinia | 3.0.3 | State management |
| Axios | 1.10.0 | HTTP client |
| Bootstrap | 5.3.7 | UI framework |
| Chart.js | 4.5.0 | Data visualization |
| Popper.js | 2.11.8 | Tooltip positioning |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│                     (Vue 3 + Bootstrap)                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 │ HTTP Requests (Axios)
                 │
┌────────────────▼────────────────────────────────────────────┐
│                      FLASK BACKEND                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Authentication Layer (Flask-Security)               │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Routes (auth_apis.py + crud_apis.py)           │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Business Logic & Models (SQLAlchemy ORM)            │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼─────┐   ┌──────▼────────┐
│   SQLite    │   │  Redis Cache  │
│  Database   │   │   (5 min TTL) │
└─────────────┘   └───────────────┘
                          │
                  ┌───────▼────────┐
                  │ Celery Workers │
                  │ (Background)   │
                  └────────────────┘
```

**Data Flow:**
1. User interacts with Vue.js frontend
2. Axios sends HTTP requests to Flask API
3. Flask-Security validates authentication tokens
4. Business logic processes requests via SQLAlchemy ORM
5. Data stored in SQLite database
6. Redis caches frequently accessed data
7. Celery handles background tasks (emails, reports)

---

## 🗄 Database Schema

### User
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,  -- Bcrypt hashed
    fs_uniquifier VARCHAR(255) UNIQUE NOT NULL,
    active BOOLEAN,
    name VARCHAR(255),
    address TEXT,
    pin VARCHAR(10)
);
```

### Role
```sql
CREATE TABLE role (
    id INTEGER PRIMARY KEY,
    name VARCHAR(80) UNIQUE NOT NULL,  -- 'admin' or 'user'
    description VARCHAR(255)
);
```

### UserRoles (Many-to-Many Junction Table)
```sql
CREATE TABLE user_roles (
    user_id INTEGER REFERENCES user(id),
    role_id INTEGER REFERENCES role(id),
    PRIMARY KEY (user_id, role_id)
);
```

### Lot (Parking Lot)
```sql
CREATE TABLE lot (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,  -- Per hour rate
    address TEXT,
    pin VARCHAR(10),
    max_spots INTEGER NOT NULL
);
```

### Spot (Parking Spot)
```sql
CREATE TABLE spot (
    id INTEGER PRIMARY KEY,
    lot_id INTEGER REFERENCES lot(id),
    status CHAR(1) DEFAULT 'A'  -- 'A' = Available, 'O' = Occupied
);
```

### Reservation
```sql
CREATE TABLE reservation (
    id INTEGER PRIMARY KEY,
    spot_id INTEGER REFERENCES spot(id),
    user_id INTEGER REFERENCES user(id),
    time_in DATETIME DEFAULT CURRENT_TIMESTAMP,
    time_out DATETIME,  -- NULL = active reservation
    rate FLOAT  -- Hourly rate at time of booking
);
```

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | ❌ |
| POST | `/api/auth/login` | Login and get auth token | ❌ |
| POST | `/logout` | Logout current user | ✅ |

**Register Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "address": "123 Main St",
  "pin": "110001"
}
```

**Login Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Login Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "roles": ["user"]
  },
  "auth_token": "WyIxIiwiJDJiJDEyJC4uLiJd..."
}
```

### Parking Lots

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/lots` | Get all parking lots | ✅ | Any |
| GET | `/api/lots/<lot_id>` | Get single lot details | ✅ | Any |
| POST | `/api/lots` | Create new parking lot | ✅ | Admin |
| PUT | `/api/lots/<lot_id>` | Update lot details | ✅ | Admin |
| DELETE | `/api/lots/<lot_id>` | Delete parking lot | ✅ | Admin |

**Create Lot Request:**
```json
{
  "name": "Downtown Parking",
  "price": 50.0,
  "address": "456 City Center",
  "pin": "110002",
  "max_spots": 20
}
```

**Get All Lots Response:**
```json
[
  {
    "id": 1,
    "name": "Downtown Parking",
    "price": 50.0,
    "address": "456 City Center",
    "pin": "110002",
    "max_spots": 20,
    "available_spots": 15,
    "occupied_spots": 5
  }
]
```

### Spots

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/lots/<lot_id>/spots` | Get all spots in a lot | ✅ |

**Response:**
```json
[
  {
    "id": 1,
    "lot_id": 1,
    "status": "A"
  },
  {
    "id": 2,
    "lot_id": 1,
    "status": "O",
    "reservation": {
      "id": 5,
      "user_id": 2,
      "time_in": "2026-03-30T10:30:00Z"
    }
  }
]
```

### Reservations

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/reservations` | Create new reservation | ✅ |
| GET | `/api/reservations` | Get all reservations | ✅ (Admin) |
| GET | `/api/users/<user_id>/reservations` | Get user's reservations | ✅ |
| PUT | `/api/reservations/<reservation_id>/end` | End reservation & pay | ✅ |
| GET | `/api/reservations/<reservation_id>/calculate_cost` | Calculate current cost | ✅ |

**Create Reservation Request:**
```json
{
  "lot_id": 1,
  "user_id": 2
}
```

**Calculate Cost Response:**
```json
{
  "reservation_id": 5,
  "time_in": "2026-03-30T10:30:00Z",
  "duration_hours": 2.5,
  "rate": 50.0,
  "total_cost": 125.0
}
```

### Users

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/api/admin/users` | Get all users with 'user' role | ✅ | Admin |

---

## 📁 Project Structure

```
vehicle_parking_app/
│
├── backend/
│   ├── app.py                    # Application entry point
│   ├── celery_app.py            # Celery configuration
│   ├── mail.py                  # Email utilities
│   ├── requirment.txt           # Python dependencies
│   │
│   ├── application/
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration (DB, Redis, Security)
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── auth_apis.py         # Authentication endpoints
│   │   ├── crud_apis.py         # CRUD operations for lots/reservations
│   │   └── task.py              # Celery background tasks
│   │
│   ├── instance/
│   │   └── securedb.sqlite3     # SQLite database file
│   │
│   └── static/                  # Static files (if any)
│
├── frontend/
│   ├── index.html               # Entry HTML
│   ├── package.json             # NPM dependencies
│   ├── vite.config.js           # Vite configuration
│   │
│   ├── src/
│   │   ├── main.js              # Vue app initialization
│   │   ├── App.vue              # Root component
│   │   │
│   │   ├── router/
│   │   │   └── index.js         # Vue Router configuration
│   │   │
│   │   ├── stores/
│   │   │   └── auth.js          # Pinia authentication store
│   │   │
│   │   ├── views/
│   │   │   ├── HomeView.vue           # Landing page
│   │   │   ├── DashboardView.vue      # Dashboard router
│   │   │   ├── AdminDashboard.vue     # Admin interface
│   │   │   ├── UserDashboard.vue      # User interface
│   │   │   ├── login.vue              # Login form
│   │   │   └── register.vue           # Registration form
│   │   │
│   │   └── components/
│   │       └── Navbar.vue       # Navigation bar
│   │
│   └── public/                  # Public assets
│
└── README.md                    # This file
```

---

## ✅ Prerequisites

Before running this application, ensure you have the following installed:

### Required Software
- **Python** 3.8 or higher ([Download](https://www.python.org/downloads/))
- **Node.js** 18.x or higher ([Download](https://nodejs.org/))
- **npm** (comes with Node.js)
- **Redis Server** ([Download](https://redis.io/download))
  - Windows: Use [Windows Subsystem for Linux (WSL)](https://redis.io/docs/getting-started/installation/install-redis-on-windows/) or [Memurai](https://www.memurai.com/)

### Optional (for email functionality)
- **SMTP Server** (Mock server on port 1025, or use [MailHog](https://github.com/mailhog/MailHog))

---

## 📥 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd vehicle_parking_app_23f1000932
```

### 2. Backend Setup

#### Navigate to backend directory
```bash
cd backend
```

#### Create Python virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Install Python dependencies
```bash
pip install -r requirment.txt
```

#### Additional dependencies (if not in requirements.txt)
```bash
pip install Flask-CORS redis celery
```

### 3. Frontend Setup

#### Navigate to frontend directory
```bash
cd ../frontend
```

#### Install NPM dependencies
```bash
npm install
```

### 4. Redis Setup

#### Windows (using WSL or Memurai)
```bash
# If using WSL
wsl
sudo service redis-server start

# Or download and install Memurai
```

#### Linux/Mac
```bash
# Start Redis server
redis-server
```

#### Verify Redis is running
```bash
redis-cli ping
# Expected output: PONG
```

---

## 🚀 Running the Application

You need to run **three separate terminals** for the application to work fully:

### Terminal 1: Backend (Flask)

```bash
cd backend
# Activate virtual environment (if created)
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

python app.py
```

**Expected Output:**
```
Successfully connected to Redis!
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Terminal 2: Frontend (Vue + Vite)

```bash
cd frontend
npm run dev
```

**Expected Output:**
```
  VITE v6.2.4  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Terminal 3: Celery Worker (Optional - for background tasks)

```bash
cd backend
# Activate virtual environment
celery -A celery_app.celery_app worker --loglevel=info
```

### Terminal 4: Celery Beat (Optional - for scheduled tasks)

```bash
cd backend
# Activate virtual environment
celery -A celery_app.celery_app beat --loglevel=info
```

---

## 🔑 Default Credentials

The application comes with a pre-configured admin account:

| Role | Email | Password |
|------|-------|----------|
| Admin | user@admin.com | 1234 |

**Note:** Regular users must register through the `/register` page.

---

## 📖 Usage Guide

### For Regular Users

#### 1. **Registration**
- Navigate to `http://localhost:5173/register`
- Fill in: Email, Password, Name, Address, PIN Code
- Click "Register"

#### 2. **Login**
- Go to `http://localhost:5173/login`
- Enter your email and password
- You'll be redirected to the User Dashboard

#### 3. **Browse Parking Lots**
- View available parking lots with real-time spot availability
- See pricing per hour

#### 4. **Make a Reservation**
- Select a parking lot
- Click "Book Now"
- System automatically assigns an available spot

#### 5. **View Reservations**
- See your active and past reservations
- Track check-in times

#### 6. **Calculate Cost**
- Click "Calculate Cost" on an active reservation
- See real-time charges based on duration

#### 7. **End Reservation**
- Click "End Reservation & Pay"
- Confirm payment (simulated)
- Spot becomes available again

#### 8. **View Analytics**
- Check your dashboard for a doughnut chart
- Compare active vs completed reservations

### For Administrators

#### 1. **Login**
- Use default admin credentials: `user@admin.com` / `1234`

#### 2. **Create Parking Lot**
- Fill in: Name, Address, PIN, Price per hour, Maximum spots
- System auto-generates the specified number of spots

#### 3. **Manage Lots**
- Edit lot details (name, price, address)
- Increase/decrease spot capacity (spots added/removed automatically)
- Delete lots (only if no active reservations)

#### 4. **View Users**
- See all registered users
- Check user details (email, name, address)

#### 5. **Monitor System**
- View bar chart showing total vs occupied spots per lot
- See all system-wide reservations

---

## ⚙️ Background Tasks

### Celery Tasks (Configured in `application/task.py`)

#### 1. **Daily Reminder Email**
- **Schedule:** 18:07 IST (6:07 PM) every day
- **Purpose:** Send reminder emails to users about parking reservations
- **Status:** Configured but requires SMTP server

#### 2. **Monthly Activity Report**
- **Schedule:** Every 30 seconds (for testing) / Monthly (production)
- **Purpose:** Generate and email monthly parking activity reports
- **Format:** HTML email with reservation statistics

#### 3. **CSV Export**
- **Trigger:** On-demand
- **Purpose:** Export reservation data to CSV and email to admins
- **Status:** Partially implemented

---

## 🔧 Configuration

### Backend Configuration (`application/config.py`)

```python
class LocalDevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///securedb.sqlite3"
    DEBUG = True
    SECRET_KEY = "this-is-a-secret-key"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "this-is-a-salt-key"
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
```

### Frontend Configuration (`src/main.js`)

```javascript
axios.defaults.baseURL = 'http://localhost:5000'
```

### Redis Configuration
- **Host:** localhost
- **Port:** 6379
- **DB:** 0
- **Cache TTL:** 300 seconds (5 minutes)

---

## 🎯 Key Features Implemented

### ✅ Core Functionality
- [x] User registration with password hashing
- [x] Token-based authentication
- [x] Role-based access control (Admin & User)
- [x] Parking lot CRUD operations
- [x] Dynamic spot generation and management
- [x] Real-time spot availability tracking
- [x] Reservation booking with auto spot assignment
- [x] Cost calculation (hours × hourly rate)
- [x] Reservation history tracking
- [x] Payment simulation

### ✅ Advanced Features
- [x] Redis caching with automatic invalidation
- [x] Celery background task integration
- [x] Email notification system (SMTP)
- [x] Admin dashboard with analytics
- [x] User dashboard with reservation tracking
- [x] Chart.js data visualization (Bar & Doughnut charts)
- [x] CORS-enabled API
- [x] Responsive Bootstrap UI

### ⚠️ Partially Implemented
- [ ] Payment gateway integration (currently simulated)
- [ ] Rate limiting
- [ ] Comprehensive error logging
- [ ] Admin route authentication enforcement
- [ ] Input validation on all fields

---

## 🐛 Known Issues & Limitations

1. **Payment System:** Currently simulated - no real payment gateway integration
2. **Email:** Requires SMTP server on localhost:1025 (use MailHog for testing)
3. **Redis Required:** Application won't start without Redis connection
4. **No Password Reset:** Users cannot reset forgotten passwords
5. **Limited Validation:** Some API endpoints lack comprehensive input validation

---

## 🛡 Security Considerations

- ✅ Passwords hashed with bcrypt
- ✅ Token-based authentication
- ✅ SQL injection protection via SQLAlchemy ORM
- ⚠️ CSRF disabled (enable in production)
- ⚠️ No rate limiting (add in production)
- ⚠️ CORS allows all origins (restrict in production)

---

## 📝 Database Initialization

The database is automatically initialized on first run with:
- Two roles: `admin` and `user`
- One admin account: `user@admin.com` / `1234`

To reset the database:
```bash
cd backend/instance
rm securedb.sqlite3
cd ..
python app.py  # Will recreate database
```

---

## 🧪 Testing the Application

### Quick Test Workflow

1. **Start all services** (Flask, Vite, Redis)
2. **Open browser** to `http://localhost:5173`
3. **Register a new user**
4. **Login as admin** (user@admin.com / 1234)
5. **Create a parking lot** (e.g., 10 spots at ₹50/hour)
6. **Logout and login as regular user**
7. **Make a reservation** at the created lot
8. **Wait a few minutes**
9. **Calculate cost** to see charges
10. **End reservation** and verify spot becomes available

---

## 📊 API Response Examples

### Success Response
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... }
}
```

### Error Response
```json
{
  "error": true,
  "message": "Error description",
  "details": "Additional error information"
}
```

---

## 🤝 Contributing

This is a project developed for [IIT Study Material/PROJECT]. For contributions or issues, please contact the project maintainer.

---

## 📄 License

This project is part of an academic assignment. All rights reserved.

---

## 👨‍💻 Author

**Project:** Vehicle Parking Management System  
**Course:** IIT Study Material  
**Year:** 2023-2024

---

## 📞 Support

For issues or questions:
1. Check this README thoroughly
2. Verify all prerequisites are installed
3. Ensure Redis is running
4. Check console logs for errors
5. Verify all services are running on correct ports

---

## 🎉 Quick Start Summary

```bash
# 1. Install dependencies
cd backend && pip install -r requirment.txt
cd ../frontend && npm install

# 2. Start Redis
redis-server

# 3. Start Backend (Terminal 1)
cd backend && python app.py

# 4. Start Frontend (Terminal 2)
cd frontend && npm run dev

# 5. Open browser
http://localhost:5173

# 6. Login as admin
Email: user@admin.com
Password: 1234
```

---

**Happy Parking! 🚗🅿️**
