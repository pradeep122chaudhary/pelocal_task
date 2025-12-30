This is a clean, professional `README.md` file tailored for your GitHub repository. It highlights the unique constraints of your project (Raw SQL and no Generic ViewSets) which is crucial for demonstrating your technical depth to the recruiters at Pelocal Fintech.

---

# 📝 To-Do List Application (Python Developer Assignment)

A robust **To-Do List web application** built with **Django** and **Django REST Framework (DRF)**. This project demonstrates the ability to handle database operations using **Raw SQL** instead of the traditional Django ORM, ensuring high performance and deep understanding of database interactions.

---

## 🚀 Project Overview

This application provides a seamless blend of **RESTful APIs** for programmatic task management and **HTML templates** for a user-friendly web interface.

### Key Constraints Followed:

* ❌ **No Django ORM:** All database interactions are handled via `connection.cursor`.
* ❌ **No Generic ViewSets:** APIs are built using `APIView` for granular control.
* ✅ **Raw SQL:** Custom queries for CRUD and table initialization.
* ✅ **Hybrid Auth:** Token-based for APIs and Session-based for UI.

---

## 🛠 Tech Stack

| Layer | Technology |
| --- | --- |
| **Language** | Python 3.x |
| **Backend** | Django |
| **API Framework** | Django REST Framework (DRF) |
| **Database** | SQLite |
| **Database Access** | Raw SQL (`connection.cursor`) |
| **Authentication** | DRF Token Auth & Django Session Auth |
| **Frontend** | HTML + Tailwind CSS |
| **Testing** | pytest, pytest-django |

---

## ✨ Features

### 🔐 Authentication

* **User Management:** Registration and Login systems.
* **Dual-Auth:** Secure token generation for API clients and session management for browser users.
* **Logout:** Secure session invalidation.

### 📋 Task Management

* **Full CRUD:** Create, Read, Update, and Delete tasks.
* **Soft Delete:** Tasks are marked as deleted rather than removed from the database.
* **Prioritization:** Assign tasks as `low`, `medium`, `high`, or `urgent`.
* **Status Tracking:** Toggle between `pending` and `completed`.

### 🖥 User Interface

* **Responsive Dashboard:** A clean UI built with Tailwind CSS.
* **Interactive Forms:** Real-time updates via API integration within templates.

---

## 📂 Project Structure

```text
todo/
├── views/
│   ├── page_views.py       # Template rendering (Login, Register, Dashboard)
│   ├── auth_api_views.py   # Authentication Logic (Register/Login/Logout)
│   └── task_api_views.py   # Task CRUD Logic (Executing Raw SQL)
├── templates/
│   └── todo/
│       ├── login.html      # User Login Page
│       ├── register.html   # User Registration Page
│       └── task_list.html  # Main Task Dashboard
├── serializers.py          # DRF Serializers (Manual data mapping)
├── init_db.py              # Raw SQL script for Table Initialization
├── db_utils.py             # Helper functions (e.g., dictfetch)
├── urls.py                 # URL routing for both APIs and Pages
├── tests/                  # Automated test cases
└── requirements.txt        # Project dependencies

```

---

## 🗄 Database Design

The application uses a custom-built `tasks` table. Below is the schema executed during initialization:

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

```

---

## ⚙️ Setup & Installation

Follow these steps to get the project running locally:

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd todo_app

```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Initialize Database

Since we are not using ORM migrations, run the custom initialization script:

```bash
python todo/init_db.py

```

### 5. Run the Server

```bash
python manage.py runserver

```

Access the app at `http://127.0.0.1:8000/`.

---
