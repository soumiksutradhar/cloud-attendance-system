# Cloud-Based Attendance System

This is a Flask-based cloud attendance tracking system with user authentication, role-based access, and automated attendance marking. The app has been Dockerized for easy deployment.

---

## Features

- User registration and login (students, teachers, admins)
- Role-based access control
- Automatic attendance marking during valid time windows
- SQLite database with Docker volume persistence
- Dockerized app for easy setup and deployment

---

## Technologies used

- Python 3.11
- Flask (Flask-Login, Flask-Bcrypt, Flask-WTF, Flask-SQLAlchemy)
- SQLite
- Docker

---

## Setup instructions

### 1. Prerequisites

- Docker installed on your machine
- Git installed

### 2. Clone the repository

```bash
git clone https://github.com/soumiksutradhar/cloud-attendance-system.git
cd attendance-system
```

### 3. Build the Docker image
```bash
docker build -t attendance-system .
```

### 4. Run the Docker container with volume for data persistance
```bash
docker run -d -p 5000:5000 -v $(pwd)/instance:/app/instance attendance-system
```

### 5. Access the app through the exposed container port
```bash
http://localhost:5000
```

---

## Project structure
<pre><code>
app/
├── __init__.py
├── decorators.py
├── forms/
│   ├── __init__.py
│   ├── attendance_forms.py
│   └── auth_forms.py
├── models/
│   ├── __init__.py
│   ├── attendance.py
│   └── user.py
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   └── main.py
├── static/
│   └── css/
│       └── styles.css
└── templates/
    ├── 403.html
    ├── home.html
    ├── layout.html
    ├── login.html
    ├── register.html
    ├── set_attendance_window.html
    └── teacher_dashboard.html
</code></pre>

---

## Future updates
- QR scanning for extra verification
- UI improvements
- QOL improvements
