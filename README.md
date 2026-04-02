# 📋 Task Management System

A full-stack task management application with a **Flask REST API** backend and a responsive frontend. Features include JWT authentication, CRUD operations, task filtering, priority levels, and real-time statistics.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.23-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔐 Authentication & Security
- **JWT Token-based Authentication** - Secure, stateless authentication
- **Password Hashing** - PBKDF2-SHA256 encryption
- **Protected API Routes** - Authorization required for all task operations
- **SQL Injection Prevention** - SQLAlchemy ORM parameterized queries
- **CORS Protection** - Configured for secure cross-origin requests

### 📝 Task Management
- **Create Tasks** - Add tasks with title, description, priority, and due date
- **Update Tasks** - Edit task details and status
- **Delete Tasks** - Remove unwanted tasks
- **Filter Tasks** - Filter by status (Pending, In Progress, Completed)
- **Priority Levels** - High, Medium, Low priority classification
- **Due Dates** - Set and track task deadlines

### 📊 Dashboard
- **Real-time Statistics** - Total, pending, in-progress, and completed task counts
- **Visual Cards** - Color-coded statistics with icons
- **Responsive Design** - Works on mobile, tablet, and desktop

### 🎨 User Interface
- **Modern Gradient Design** - Beautiful purple gradient background
- **Smooth Animations** - Slide-up effects and hover transitions
- **Mobile-First** - Fully responsive Bootstrap 5 layout
- **Interactive Elements** - Floating action button, modal forms
- **Empty States** - Helpful messages when no tasks exist

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose | Version |
|------------|---------|---------|
| **Flask** | Web framework | 3.0.0 |
| **SQLAlchemy** | Database ORM | 2.0.23 |
| **Flask-JWT-Extended** | JWT authentication | 4.5.3 |
| **Marshmallow** | Data validation & serialization | 3.20.1 |
| **Flask-CORS** | Cross-origin resource sharing | 4.0.0 |
| **Werkzeug** | Password hashing utilities | 3.0.1 |

### Frontend
| Technology | Purpose | Version |
|------------|---------|---------|
| **HTML5** | Structure | - |
| **CSS3** | Styling & animations | - |
| **JavaScript (ES6+)** | Interactivity | - |
| **Bootstrap 5** | UI framework | 5.3.0 |
| **Font Awesome** | Icons | 6.4.0 |

### Database
- **SQLite** - Development database (can be switched to PostgreSQL/MySQL)

---

## 📁 Project Structure

```
task-management/
│
├── app.py                      # Flask backend application
├── requirements.txt            # Python dependencies
├── tasks.db                    # SQLite database (auto-generated)
│
├── static/
│   └── index.html             # Frontend application
│
├── README.md                  # This file
├── QUICK_START.md            # Quick start guide
└── .gitignore                # Git ignore file
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+** installed
- **pip** package manager
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

#### 1. Clone or Download the Project
```bash
# Create project directory
mkdir task-management
cd task-management
```

#### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
marshmallow==3.20.1
Flask-Marshmallow==1.2.0
marshmallow-sqlalchemy==0.29.0
Flask-JWT-Extended==4.5.3
Flask-CORS==4.0.0
Werkzeug==3.0.1
SQLAlchemy==2.0.23
```

#### 4. Run the Backend
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

#### 5. Open the Frontend

**Option A: Using PyCharm (or similar IDE)**
- Right-click on `static/index.html`
- Select "Open in Browser" or use the built-in server

**Option B: Using Python HTTP Server**
```bash
# In a NEW terminal (keep Flask running in the first one)
cd task-management
python -m http.server 8000
```
Then open: `http://localhost:8000/static/index.html`

**Option C: Direct File Access**
- Navigate to `static/index.html` in your file explorer
- Double-click to open in browser

---

## 📖 Usage Guide

### First Time Setup

1. **Open the Application**
   - Navigate to `http://localhost:8000/static/index.html`

2. **Register an Account**
   - Click "Register" link
   - Enter username, email, and password
   - Click "Register" button

3. **Login**
   - Enter your username and password
   - Click "Login"
   - You'll be redirected to the dashboard

### Creating Tasks

1. **Click the + Button** (floating button in bottom-right)
2. **Fill in Task Details:**
   - Title (required)
   - Description (optional)
   - Priority (High/Medium/Low)
   - Status (Pending/In Progress/Completed)
   - Due Date (optional)
3. **Click "Save Task"**

### Managing Tasks

- **Edit Task**: Click the blue edit icon (✏️)
- **Delete Task**: Click the red trash icon (🗑️)
- **Filter Tasks**: Click filter buttons (All/Pending/In Progress/Completed)

### Viewing Statistics

The dashboard displays real-time statistics:
- **Total Tasks**: All tasks count
- **Pending**: Tasks not started
- **In Progress**: Tasks being worked on
- **Completed**: Finished tasks

---

## 🔌 API Documentation

### Base URL
```
http://127.0.0.1:5000/api
```

### Authentication Endpoints

#### Register User
```http
POST /api/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}

Response (201):
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2026-01-18T12:00:00"
  }
}
```

#### Login
```http
POST /api/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepassword123"
}

Response (200):
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

### Task Endpoints (Require JWT Token)

**All task endpoints require Authorization header:**
```
Authorization: Bearer <your_jwt_token>
```

#### Get All Tasks
```http
GET /api/tasks
Authorization: Bearer <token>

# Optional query parameters:
GET /api/tasks?status=pending
GET /api/tasks?priority=high

Response (200):
[
  {
    "id": 1,
    "title": "Complete project documentation",
    "description": "Write comprehensive README",
    "priority": "high",
    "status": "in_progress",
    "due_date": "2026-01-25T17:00:00",
    "user_id": 1,
    "created_at": "2026-01-18T12:00:00",
    "updated_at": "2026-01-18T14:30:00"
  }
]
```

#### Get Single Task
```http
GET /api/tasks/{id}
Authorization: Bearer <token>

Response (200):
{
  "id": 1,
  "title": "Complete project documentation",
  ...
}
```

#### Create Task
```http
POST /api/tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Learn Flask",
  "description": "Complete Flask tutorial",
  "priority": "medium",
  "status": "pending",
  "due_date": "2026-01-30T18:00:00"
}

Response (201):
{
  "message": "Task created successfully",
  "task": { ... }
}
```

#### Update Task
```http
PUT /api/tasks/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Learn Flask (Updated)",
  "status": "in_progress"
}

Response (200):
{
  "message": "Task updated successfully",
  "task": { ... }
}
```

#### Delete Task
```http
DELETE /api/tasks/{id}
Authorization: Bearer <token>

Response (200):
{
  "message": "Task deleted successfully"
}
```

#### Get Statistics
```http
GET /api/tasks/stats
Authorization: Bearer <token>

Response (200):
{
  "total": 10,
  "pending": 3,
  "in_progress": 4,
  "completed": 3
}
```

### Error Responses

```json
// 400 Bad Request
{
  "error": "Title is required"
}

// 401 Unauthorized
{
  "error": "Invalid credentials"
}

// 404 Not Found
{
  "error": "Task not found"
}

// 500 Internal Server Error
{
  "error": "Database error message"
}
```

---

## 🔒 Security Features

### 1. Password Security
- **Hashing Algorithm**: PBKDF2-SHA256
- **Iterations**: 260,000 rounds
- **Salt**: Automatically generated per password
- Passwords never stored in plain text

**Example:**
```python
# Plain password
"mypassword123"

# Stored in database
"pbkdf2:sha256:260000$K5tGxL7W$3f8d9c2b1a..."
```

### 2. JWT Authentication
- **Token Expiration**: 24 hours
- **Algorithm**: HS256
- **Secret Key**: Configurable (change in production!)
- Stateless - no server-side session storage

**Token Structure:**
```
Header.Payload.Signature
eyJhbGc... (Base64 encoded)
```

### 3. SQL Injection Prevention
- All queries use SQLAlchemy ORM
- Automatic parameterization
- No string concatenation in queries

**Safe Example:**
```python
# ✅ Safe - SQLAlchemy parameterizes automatically
user = User.query.filter_by(username=username).first()

# ❌ Vulnerable - Don't do this
query = f"SELECT * FROM users WHERE username = '{username}'"
```

### 4. CORS Configuration
- Allows cross-origin requests from frontend
- Can be restricted to specific domains in production

### 5. Authorization
- Tasks can only be accessed by their owner
- User ID extracted from JWT token
- Database queries filter by user_id

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'pending',
    due_date DATETIME,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### Relationships
```
User (1) ──────── (Many) Tasks

One user can have multiple tasks
Each task belongs to one user
Cascade delete: Deleting user deletes their tasks
```

---

## 🧪 Testing

### Manual Testing with cURL

**Register:**
```bash
curl -X POST http://127.0.0.1:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@test.com","password":"test123"}'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123"}'
```

**Get Tasks (replace TOKEN):**
```bash
curl -X GET http://127.0.0.1:5000/api/tasks \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

**Create Task:**
```bash
curl -X POST http://127.0.0.1:5000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -d '{"title":"Test Task","priority":"high"}'
```

### Testing with Postman
1. Import the API endpoints
2. Set up environment variable for token
3. Test all CRUD operations
4. Verify error handling

---

## ⚙️ Configuration

### Change JWT Secret Key (IMPORTANT for Production!)
```python
# In app.py, line 13
app.config['JWT_SECRET_KEY'] = 'your-super-secret-key-here-change-me'
```

### Change Database (PostgreSQL Example)
```python
# In app.py, line 12
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/taskdb'
```

### Adjust Token Expiration
```python
# In app.py, line 14
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=48)  # 48 hours
```

---

## 🐛 Troubleshooting

### Issue: "Module not found" error
**Solution:**
```bash
# Make sure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Port 5000 already in use"
**Solution:**
```bash
# Kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:5000 | xargs kill -9
```

### Issue: "401 Unauthorized" on all requests
**Solution:**
1. Check if you're logged in
2. Clear browser localStorage (F12 → Application → Local Storage → Clear)
3. Login again

### Issue: Tasks not saving
**Solution:**
1. Check browser console for errors (F12 → Console)
2. Check Flask terminal for error messages
3. Verify API_URL in index.html points to correct backend

### Issue: Database errors
**Solution:**
```bash
# Delete and recreate database
rm tasks.db
python app.py  # Database will be auto-created
```


## 📝 License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 👨‍💻 Author

Muntaha Asif
- GitHub: (https://github.com/Muntaha-Asif)
- LinkedIn: (https://www.linkedin.com/in/muntaha-asif-84156732a/)

---

## 🙏 Acknowledgments

- **Flask** team for the excellent web framework
- **Bootstrap** for the responsive UI components
- **Font Awesome** for the beautiful icons
- **SQLAlchemy** for the powerful ORM
- **Stack Overflow** community for troubleshooting help

---


## ⭐ Star this Repository

If you found this project helpful, please give it a ⭐ on GitHub!

---

**Built with ❤️ using Flask, Python, and modern web technologies**

*Last Updated: January 2026*
