# DataVault 🔐

> **Own your data. Control who sees it. Earn from it.**

DataVault is a consent-first personal data marketplace where users upload and monetize their data, while brands pay for anonymized, aggregated insights. Raw data never leaves the vault.

---

# 🌍 The Problem

Google, Meta, and data brokers scrape your digital footprints for free and sell them for billions. **You get zero.**

---

# 💡 The Solution

DataVault flips the model:

- You upload your data into an encrypted vault
- Brands pay to ask specific questions about it
- You get paid instantly when you accept
- A **Kill Switch** auto-revokes access after 24 hours
- Brands only see anonymized, aggregated signals — never raw data

---

# ✨ Features

| Feature | Description |
|---|---|
| 🔐 AES-256 Encryption | Every file encrypted at upload. Decrypted only during computation. |
| 💰 Instant Wallet | Accept a request, earn instantly. Platform takes 10% cut. |
| 🔪 Kill Switch | Access auto-expires after 24 hours. No continuous tracking. |
| 📊 Signal Engine | Brands get aggregated percentages only. Never raw data. |
| ✅ Consent First | Every request needs explicit user approval. No silent tracking. |
| 🗑️ Delete Anytime | Full DPDP-compliant data deletion. |

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Auth | JWT + bcrypt |
| Encryption | Fernet AES-256 |
| Scheduling | APScheduler (Kill Switch) |
| Signal Engine | Pandas |
| Frontend | HTML + Tailwind CSS + Vanilla JS |
| Deployment | Docker + Docker Compose |
| API Docs | Swagger UI |

---

# 🚀 Local Setup

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/datavault.git
cd datavault
```

---

## 2. Create virtual environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create PostgreSQL database

Create a PostgreSQL database named:

```sql
CREATE DATABASE datavault;
```

---

## 5. Setup environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/datavault
SECRET_KEY=your-secret-key
ENCRYPTION_KEY=your-fernet-key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 6. Generate encryption key

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the generated key into:

```env
ENCRYPTION_KEY=
```

---

## 7. Run the backend server

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

---

## 8. Open the frontend

Open:

```text
frontend/index.html
```

using VS Code Live Server.

---

# 🐳 Docker Setup (Optional)

## Build and start containers

```bash
docker-compose up --build
```

---

## Stop containers

```bash
docker-compose down
```

---

# 📁 Project Structure

```text
datavault/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── scheduler.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── brand.py
│   │   ├── data_request.py
│   │   └── uploaded_file.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── upload.py
│   │   ├── requests.py
│   │   └── wallet.py
│   │
│   ├── core/
│   │   ├── security.py
│   │   ├── encryption.py
│   │   ├── signals.py
│   │   └── config.py
│   │
│   └── services/
│       ├── signal_engine.py
│       └── kill_switch_service.py
│
├── frontend/
│   ├── index.html
│   │
│   ├── pages/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── user-dashboard.html
│   │   ├── brand-dashboard.html
│   │   └── upload.html
│   │
│   ├── js/
│   │   ├── api.js
│   │   ├── auth.js
│   │   └── dashboard.js
│   │
│   └── css/
│       └── styles.css
│
├── uploads/
├── .env
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

# 🎯 Demo Flow

## User Flow

1. Register as a user
2. Upload shopping or fitness CSV data
3. Files get encrypted instantly
4. User stores data inside personal vault

---

## Brand Flow

1. Register as a brand
2. Create a data request
3. Select:
   - signal type
   - demographics
   - offer amount
4. Send request to users

---

## Consent Flow

1. User receives notification
2. User sees:
   - brand name
   - exact query
   - payment offered
3. User accepts or rejects

---

## Insight Flow

1. Wallet credited instantly
2. Platform takes 10% commission
3. Brand receives:
   - aggregated percentages
   - anonymized trends
4. Raw files never exposed

---

## Kill Switch Flow

1. Access expires automatically after 24 hours
2. Background scheduler revokes permissions
3. Continuous tracking prevented

---

# 📊 Sample CSV Files

## shopping.csv

```csv
date,product,category,price,brand
2024-01-15,Running Shoes,footwear,2800,Nike
2024-01-22,Water Bottle,accessories,450,Generic
2024-02-01,Track Pants,clothing,1200,Adidas
2024-02-10,Running Shoes,footwear,3500,Asics
2024-02-18,Socks,accessories,299,Nike
```

---

## fitness.csv

```csv
date,activity,duration_mins,distance_km,runs_per_week
2024-01-15,running,35,5.2,4
2024-01-17,running,28,4.1,4
2024-01-20,cycling,45,12.0,4
2024-01-22,running,40,6.0,4
2024-01-25,running,32,4.8,4
```

---

# 🔒 Security Architecture

## Encryption

- AES-256 encryption using Fernet
- Encryption performed during upload
- Files decrypted only during computation

---

## Authentication

- JWT token authentication
- Password hashing with bcrypt
- Role-based access control

---

## Privacy

- No raw data sharing
- Only aggregated insights exposed
- Explicit consent required for every request

---

# 📈 Example Brand Insights

Brands receive signals like:

```text
72% of users aged 18-25 buy running products monthly
61% prefer Nike over Adidas
48% run more than 3 times per week
```

NOT:
- names
- emails
- raw CSVs
- personal identities

---

# 🗑️ Data Deletion

Users can:
- permanently delete uploaded files
- revoke brand access instantly
- close account anytime

Designed with:
- DPDP Act (India)
- GDPR-style consent principles

---

# 📄 API Documentation

Once backend is running, visit:

```text
https://datavault-s9lc.onrender.com/docs
```

Interactive Swagger documentation available for all endpoints.

---

# 🔮 Future Improvements

- Stripe payment integration
- Blockchain audit logs
- Differential privacy
- AI-powered signal generation
- Kubernetes deployment
- Multi-cloud storage
- Real-time streaming insights

---

# 👨‍💻 Built By

Built as a production-style full-stack project demonstrating:

- FastAPI backend architecture
- encryption systems
- consent-first data marketplaces
- background scheduling
- secure APIs
- data privacy engineering
- production-ready backend design

---

# ⭐ Why This Project Stands Out

This is not a simple CRUD project.

DataVault demonstrates:
- backend engineering
- security engineering
- data privacy architecture
- scheduling systems
- encryption workflows
- marketplace logic
- production-grade API development

Perfect for:
- MLOps portfolios
- Backend engineering portfolios
- Data engineering portfolios
- Startup internship applications

---