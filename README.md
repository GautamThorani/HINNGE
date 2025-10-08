# 🔒 HENNGE Security Platform
A **modern, microservices-based enterprise security platform** built to showcase secure authentication, real-time monitoring, and MFA integration — developed as a **full-stack security solution** inspired by enterprise use cases.

---

## 🏆 Key Highlights

- ✅ Production-grade **microservices architecture**  
- 🔐 **Multi-Factor Authentication (MFA)** with TOTP  
- 📊 **Real-time security event logging & monitoring**  
- 👥 Full-featured **user management**  
- 🧠 Built with modern, scalable **FastAPI + React + PostgreSQL + Docker**

---

## 🏗️ System Architecture

### Backend Microservices
| Service               | Port | Technology         | Responsibility                         |
|-----------------------|------|--------------------|------------------------------------------|
| API Gateway           | 8000 | FastAPI            | Routing, CORS, aggregation              |
| Auth Service          | 8001 | FastAPI + JWT      | Authentication, token lifecycle         |
| User Service          | 8002 | FastAPI + DB       | User profiles, credentials              |
| MFA Service           | 8003 | FastAPI + pyotp    | Multi-factor authentication             |
| Audit Service         | 8004 | FastAPI + DB       | Security event logging                  |
| PostgreSQL Database   | 5432 | PostgreSQL         | Persistent storage                      |

### Frontend
- **React 18** with **TypeScript**
- **Material UI** for enterprise-grade design
- **Vite** for fast development builds
- **Context API** for state management
- **Axios** for secure API communication

---

## ⚡ Core Features

### 🔐 Authentication & Security
- Secure login with JWT tokens and token expiration  
- MFA (TOTP) setup and verification flow  
- Password policies for enterprise security  
- Session & token lifecycle management  

### 📈 Audit & Monitoring
- Real-time event logging for every security-sensitive action  
- Searchable audit trails with IP & timestamp tracking  
- Security metrics & insights dashboard  

### 👥 User Management
- User registration & profile handling  
- Account activity history and status tracking  
- Secure credential storage

### 🛡️ Security Dashboard
- Real-time security score indicators  
- Threat alerts & activity feed  
- MFA status and recommendations  

---

## 🧰 Tech Stack

| Layer             | Technology                          |
|--------------------|-------------------------------------|
| Backend            | FastAPI, JWT, pyotp, bcrypt         |
| Frontend           | React, Vite, Material UI, Axios     |
| Database           | PostgreSQL 15                       |
| Deployment         | Docker & Docker Compose            |
| Security           | MFA, JWT, CORS, SQLModel ORM       |

---

## 🐳 Deployment

### **Prerequisites**
- Docker & Docker Compose
- Node.js 18+ (for frontend development)

### **One Command Start**
```bash
docker-compose up -d


🔐 Security Implementations

JWT authentication with 30-min expiration

MFA with TOTP (RFC 6238 compliant)

Password hashing (bcrypt) & strong policy enforcement

CORS protection and SQL injection prevention

XSS protection via React escaping

Strict security headers (HSTS, X-Frame-Options, etc.)


📈 Performance Optimizations

Strategic DB indexing for frequent queries

Connection pooling & optimized SQL joins

Frontend code splitting with React.lazy()

Vite build optimizations for fast load times


📁 Project Structure
hennge-security-platform/
├── backend/
│   ├── api-gateway/
│   ├── auth-service/
│   ├── user-service/
│   ├── mfa-service/
│   ├── audit-service/
│   └── init-db/
├── frontend/
│   ├── src/
│   ├── pages/
│   ├── components/
│   └── contexts/
├── docker-compose.yml
└── README.md


🌍 Future Enhancements

✅ Admin dashboard with role-based access

🔔 Email-based MFA recovery

📊 Advanced security analytics & risk scoring

☁️ Cloud deployment (Kubernetes / AWS ECS)

👨‍💻 Author & Purpose

This project is built to demonstrate full-stack engineering & security design capabilities for enterprise-level systems — a showcase project for HENNGE Internship Application.
