# 🏨 Hostel Management System

A full-stack **Role-Based Hostel Management System** built using **Django REST Framework (DRF)** and **React (Bootstrap UI)** with **JWT Authentication**.

This project demonstrates **real-world backend architecture**, **secure permission handling**, and **role-based complaint workflow management**.

---

## 🚀 Features

---

### 🔐 Authentication & Role Management

- JWT-based authentication
- Custom User Model
- Role-based authorization system

Supported Roles:

- 👨‍💼 **Admin**
- 🎓 **Student**
- 🧑‍✈️ **Warden**

---

### 👨‍💼 Admin Capabilities

Admin controls the entire hostel ecosystem:

- Create Students & Wardens
- Create Hostels
- Create Rooms under Hostels
- Allocate Students → Rooms
- Assign Wardens → Hostels
- View and manage all complaints

---

### 🎓 Student Capabilities

Students can:

- Login securely
- Raise complaints
- Track complaint status
- View only their own complaints

Complaint automatically links to:

- Student account
- Hostel (via Room Allocation)

---

### 🧑‍✈️ Warden Capabilities

Wardens can:

- View complaints belonging to their hostel
- Update complaint status:
  - OPEN
  - IN_PROGRESS
  - RESOLVED

---

## 💻 Frontend

A lightweight **React + Bootstrap dashboard** is included to demonstrate backend functionality.

Features:

- Login UI
- Student Complaint Dashboard
- Warden Complaint Management Panel
- Admin Registration Panel (Student / Warden creation)

---

## 🧩 Tech Stack

### Backend
- Django
- Django REST Framework
- Simple JWT Authentication
- Custom Permission System

### Frontend
- React (Vite)
- Bootstrap 5
- Axios

### Database
- SQLite (Development)

---

## 📸 Screenshots

### 🔐 Authentication

![Login Screenshot](screenshots/login.png)

---

### 🎓 Student Dashboard

![Student Dashboard](screenshots/student-dashboard.png)

---

### 🧑‍✈️ Warden Complaint Panel

![Warden Dashboard](screenshots/warden-dashboard.png)

---

## 📁 Project Structure

Hostel_Management_DRF/
│
├── accounts/ # User model, auth, roles
├── hostels/ # Hostel & Warden mapping
├── rooms/ # Room & Student allocation
├── complaints/ # Complaint workflow system
├── common/ # Constants & permissions
├── config/ # Settings & root URLs
│
├── frontend/ # React dashboard
├── requirements.txt
└── manage.py

---

## 🔑 API Endpoints Overview

### Authentication

POST /api/auth/login/
POST /api/auth/refresh/
GET /api/auth/me/


---

### Admin APIs

POST /api/auth/create-student/
POST /api/auth/create-warden/
POST /api/hostels/
POST /api/rooms/
POST /api/rooms/allocate/


---

### Complaint APIs

POST /api/complaints/ → Student creates complaint
GET /api/complaints/ → Role-based complaint listing
PATCH /api/complaints/{id}/ → Warden/Admin updates status


---

## 🛡 Permission Logic

| Role | View Complaints | Create Complaints | Update Complaints |
|--------|----------------|------------------|-------------------|
| Admin | All | ❌ | ✅ |
| Student | Own Only | ✅ | ❌ |
| Warden | Hostel Only | ❌ | ✅ |

---

## ⚙️ Setup Instructions

---

### 1️⃣ Clone Repository

git clone https://github.com/Arman1263/Hostel-Management-DRF-Porject.git
cd Hostel-Management-DRF-Porject


---

### 2️⃣ Create Virtual Environment

python -m venv venv


Activate:

Windows:
venv\Scripts\activate


Linux / Mac:
source venv/bin/activate


---

### 3️⃣ Install Dependencies

pip install -r requirements.txt


---

### 4️⃣ Environment Variables

Create `.env` file:

SECRET_KEY=your-secret-key
DEBUG=True


---

### 5️⃣ Apply Migrations

python manage.py migrate


---

### 6️⃣ Create Admin User

python manage.py createsuperuser


---

### 7️⃣ Run Backend Server

python manage.py runserver


---

### 8️⃣ Run Frontend

cd frontend
npm install
npm run dev


---

## 🧪 Demo Workflow

1. Admin creates hostel & rooms  
2. Admin assigns:
   - Students → Rooms  
   - Wardens → Hostels  
3. Student raises complaint  
4. Warden resolves complaint  

---

## 📚 Learning Outcomes

This project demonstrates:

- Custom Authentication System
- Role-Based Access Control
- Relational Database Design
- REST API Architecture
- Full-Stack Integration
- Real-world Workflow Modeling

---

## 👨‍💻 Author

**Arman Shikalgar**

AI & Data Science Student  
Python Developer | Backend Enthusiast  

GitHub:  
https://github.com/Arman1263
✅ Now you can:

git add README.md
git commit -m "Updated professional README"
git push
