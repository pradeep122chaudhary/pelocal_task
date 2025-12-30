# 📝 To-Do List Application  
**Python Developer Assignment – Pelocal Fintech Pvt. Ltd.**

---

## 1. Project Overview

This project is a **To-Do List web application** developed using **Python, Django, and Django REST Framework**.  
It provides **RESTful APIs** for managing tasks and **HTML templates** for user interaction.

The application strictly follows the assignment constraints:

- ❌ Django ORM is **not used**
- ❌ Generic ViewSets are **not used**
- ✅ Raw SQL is used for all database operations
- ✅ REST APIs + Template integration
- ✅ SQLite database

---

## 2. Tech Stack

| Layer | Technology |
|-----|-----------|
| Language | Python 3.x |
| Backend | Django |
| API Framework | Django REST Framework |
| Database | SQLite |
| Database Access | Raw SQL (`connection.cursor`) |
| Authentication | DRF Token Auth (APIs), Django Session Auth (Templates) |
| Frontend | HTML + Tailwind CSS |
| Testing | pytest, pytest-django |

---

## 3. Features Implemented

### Authentication
- User registration
- User login
- Token-based authentication for APIs
- Session-based authentication for template pages
- Secure logout

### Task Management
- Create task
- Retrieve tasks (user-specific)
- Update task
- Delete task (soft delete)
- Task priority & status support

### UI
- Login page
- Register page
- Task dashboard (protected)
- Tasks created/updated via APIs from templates

---

## 4. Project Structure
todo/
├── views/
│ ├── page_views.py # Template views (Home, Login, Register)
│ ├── auth_api_views.py # Auth APIs (Register/Login/Logout)
│ └── task_api_views.py # Task CRUD APIs (Raw SQL)
│
├── templates/
│ └── todo/
│ ├── login.html
│ ├── register.html
│ └── task_list.html
│
├── serializers.py # DRF Serializer (non-ORM)
├── init_db.py # Raw SQL table creation
├── db_utils.py # dictfetch helpers
├── urls.py
├── tests/ # pytest test cases
├── requirements.txt
└── README.md


---

## 5. Database Design (Raw SQL)

### `tasks` Table Schema

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    status TEXT CHECK(status IN ('pending', 'completed')),
    priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'urgent')),
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    is_deleted BOOLEAN DEFAULT 0
);

## 6. Project Setup & Run Instructions

```bash
# Clone repository
git clone <repository_url>
cd todo_app

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create database tables
python todo/init_db.py

# Run server
python manage.py runserver
