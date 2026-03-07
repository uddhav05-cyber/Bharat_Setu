<p align="center">
  <h1 align="center">🇮🇳 भारत-सेतु (Bharat-Setu)</h1>
  <p align="center"><strong>Unified Rural Intelligence Platform</strong></p>
  <p align="center">
    Carbon-Kosh · Gram-Twin · Migration-Shield<br/>
    <em>Built entirely with free & open-source technologies</em>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" />
  <img src="https://img.shields.io/badge/Tests-76%20passing-brightgreen?style=flat-square" />
</p>

---

## 📋 What is Bharat-Setu?

Bharat-Setu is a **₹0-cost pilot-ready** platform that connects India's rural economy through three integrated modules:

| Module | Purpose | Key Feature |
|--------|---------|-------------|
| 🌿 **Carbon-Kosh** | Satellite-verified carbon credits | Traffic Light fraud detection (GREEN/YELLOW/RED) |
| 🗺️ **Gram-Twin** | Digital twin for ecological planning | Village-level GeoJSON aggregation + NDVI hotspots |
| 🛡️ **Migration-Shield** | Boolean threshold crisis detection | One-strike alerting (rainfall, water, health, crop, debt) |

Every AWS service has been replaced with a **free, open-source alternative**:

| AWS Service | Bharat-Setu Replacement |
|-------------|------------------------|
| Lambda + API Gateway | FastAPI + Uvicorn |
| Aurora PostgreSQL | SQLite + SQLAlchemy |
| S3 | Local filesystem (`storage/`) |
| Cognito | PyJWT + bcrypt |
| EventBridge | In-process pub/sub event bus |
| SNS/SES | Console logging (pilot) |
| Bedrock (LLM) | Keyword-based intent extraction |
| SageMaker | NumPy calculations |

---

## 🏗️ Architecture

```
bharat-setu/
├── backend/                  # FastAPI application
│   ├── main.py               # App entry point + demo data seeding
│   ├── config.py             # Pydantic settings (env vars)
│   ├── database.py           # SQLite + SQLAlchemy setup
│   ├── auth/
│   │   ├── jwt_handler.py    # JWT token generation (PyJWT)
│   │   └── rbac.py           # Role-based access control
│   ├── models/               # 6 SQLAlchemy data models
│   │   ├── user.py           # Farmers, VLEs, Officials, Admins
│   │   ├── farm_plot.py      # GeoJSON geometry, NDVI history
│   │   ├── verification.py   # Satellite verification results
│   │   ├── certificate.py    # GCP-compliant payment certificates
│   │   ├── village_cluster.py# Vital signs for crisis detection
│   │   └── crisis_alert.py   # Boolean threshold alerts
│   ├── services/             # 10 business logic services
│   │   ├── satellite_service.py    # Mock Sentinel-2/1 imagery
│   │   ├── traffic_light_service.py# Fraud detection protocol
│   │   ├── verification_service.py # End-to-end verification pipeline
│   │   ├── threshold_service.py    # Boolean crisis detection
│   │   ├── certificate_service.py  # PDF generation (ReportLab)
│   │   ├── voice_service.py        # Mock voice intent extraction
│   │   ├── escrow_service.py       # Settlement orchestration
│   │   ├── twin_service.py         # Village digital twin GeoJSON
│   │   ├── hotspot_service.py      # NDVI degradation detection
│   │   └── alert_service.py        # Notification formatting
│   ├── adapters/
│   │   └── payment_adapter.py      # Mock e-RUPI + PFMS gateways
│   ├── events/
│   │   └── event_bus.py            # In-process pub/sub
│   ├── routers/              # 8 API route groups
│   │   ├── auth.py           # Register, Login, Refresh
│   │   ├── farms.py          # CRUD farm plots
│   │   ├── verification.py   # Trigger & check verifications
│   │   ├── alerts.py         # Crisis alert management
│   │   ├── dashboard.py      # Metrics, crisis map, export
│   │   ├── voice.py          # Voice command processing
│   │   ├── certificates.py   # Certificate CRUD + PDF download
│   │   └── twin.py           # Digital twin + hotspots
│   ├── tests/                # 76 unit tests
│   │   ├── test_traffic_light.py
│   │   ├── test_threshold.py
│   │   ├── test_verification.py
│   │   └── test_escrow.py
│   └── requirements.txt
├── frontend/                 # React admin dashboard (Vite)
│   └── src/
│       ├── App.jsx           # Sidebar navigation
│       ├── index.css         # Dark-mode design system
│       └── pages/
│           ├── Dashboard.jsx     # KPI cards + module status
│           ├── CrisisMap.jsx     # Village health monitoring
│           ├── TrafficLight.jsx  # VLE fraud detection UI
│           └── DataExport.jsx    # CSV download
├── farmer-app/               # React PWA Farmer & VLE Client (Vite)
│   └── src/
│       ├── App.jsx           # Router
│       ├── index.css         # Earth-toned glassmorphism UI
│       ├── api.js            # Axios backend integration
│       └── pages/
│           ├── Login.jsx     # Phone authentication
│           └── Dashboard.jsx # Plot tracking & Voice PTT Interface
└── storage/                  # Local file storage (replaces S3)
    ├── satellite/
    ├── certificates/
    └── evidence/
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**

### 1. Clone the repository

```bash
git clone https://github.com/uddhav05-cyber/Bharat_Setu.git
cd Bharat_Setu
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the backend server
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

The backend will:
- Create the SQLite database automatically
- Seed demo data (users, farms, village clusters)
- Start serving on **http://localhost:8000**
- Swagger UI available at **http://localhost:8000/docs**

### 3. Admin Dashboard Setup

```bash
cd frontend
npm install
npm run dev
```

Admin Dashboard available at **http://localhost:5173**

### 4. Farmer & VLE Client App Setup

The Farmer App is built as a mobile-first React PWA featuring the Push-to-Talk voice interface.

```bash
cd farmer-app
npm install
npm run dev
```

Farmer App available at **http://localhost:5174**

### 5. Run Tests

```bash
cd backend
python -m pytest tests/ -v
```

---

## 🔑 Demo Credentials

| Role | Phone | Password |
|------|-------|----------|
| Admin | `9000000001` | `admin123` |
| VLE | `9000000002` | `vle123` |
| Farmer | `9000000003` | `farmer123` |
| Sarpanch | `9000000005` | `sarpanch123` |
| District Official | `9000000006` | `official123` |

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register new user |
| `POST` | `/auth/login` | Login (returns JWT) |
| `POST` | `/auth/refresh` | Refresh access token |

### Carbon-Kosh (Farm Verification)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/farms/` | Register a farm plot |
| `GET` | `/farms/` | List farm plots |
| `POST` | `/verify/{farm_plot_id}` | Trigger satellite verification |
| `GET` | `/verify/{id}/status` | Check verification status |

### Certificates & Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/certificates/generate` | Generate certificate for GREEN verification |
| `GET` | `/certificates/` | List certificates |
| `GET` | `/certificates/{id}/download` | Download certificate PDF |

### Migration-Shield (Crisis Detection)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/alerts/check/{village_id}` | Run Boolean threshold check |
| `GET` | `/alerts/` | List active crisis alerts |

### Gram-Twin (Digital Twin)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/twin/{village_id}` | Get village digital twin GeoJSON |
| `GET` | `/twin/{village_id}/hotspots` | Get degradation hotspots |

### Voice & Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/voice/process` | Process transcribed voice input |
| `GET` | `/dashboard/metrics` | Dashboard KPIs |
| `GET` | `/dashboard/crisis-map` | Crisis map village data |
| `GET` | `/dashboard/export` | Export data as CSV |

> 📖 Full interactive API documentation: **http://localhost:8000/docs**

---

## 🚦 Traffic Light Protocol

The core fraud detection mechanism for VLE (Village-Level Entrepreneur) verification:

```
VLE submits biomass estimate
        ↓
Satellite acquires Sentinel-2/1 imagery
        ↓
Calculate variance = |VLE - Satellite| / Satellite × 100
        ↓
┌─────────────────────────────────────────────┐
│  < 10%  →  🟢 GREEN  →  Auto-approve       │
│ 10-30%  →  🟡 YELLOW →  Flag for call      │
│  > 30%  →  🔴 RED    →  Freeze account     │
└─────────────────────────────────────────────┘
        ↓
Trust score updated: GREEN +2 / RED -15
Commission: GREEN → Approved / RED → Forfeited
Account suspended if trust < 40%
```

---

## 🛡️ Boolean Threshold Crisis Detection

One-strike rule — any single breach triggers an alert:

| Threshold | Critical Trigger | Data Source |
|-----------|-----------------|-------------|
| 🌧️ Rainfall | < 50% of normal | IMD API (mocked) |
| 💧 Water Access | < 30% households | Census + Ground |
| 🏥 Health Shock | Expenditure > Income | HMIS (mocked) |
| 🌾 Crop Failure | NDVI decline > 30% | Sentinel-2 |
| 💰 Debt Crisis | Debt/Income > 2.0 | SHG reports |

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `PILOT` | `PILOT` or `PRODUCTION` |
| `DATABASE_URL` | `sqlite:///./bharat_setu.db` | Database connection |
| `SECRET_KEY` | (generated) | JWT signing key |
| `PAYMENT_ADAPTER` | `MOCK` | `MOCK` or `LIVE` |
| `STORAGE_BASE_PATH` | `./storage` | Local file storage path |

---

## 🧪 Test Coverage

**76 tests** across 4 test suites:

| Suite | Tests | Covers |
|-------|-------|--------|
| `test_traffic_light.py` | 19 | Variance calculation, GREEN/YELLOW/RED status, trust scores, commission, suspension |
| `test_threshold.py` | 17 | Individual thresholds, one-strike logic, boundary values, alert metadata |
| `test_verification.py` | 16 | NDVI calculation, SAR biomass, carbon sequestration formula, crop-type factors |
| `test_escrow.py` | 12 | Mock payment adapter, e-RUPI/PFMS routing, audit trail, voucher codes |

---

## 🎨 Admin Dashboard

The React dashboard provides 4 pages:

- **📊 Dashboard** — KPI cards (farmers, VLEs, carbon credits, critical villages), module status progress bars
- **🗺️ Crisis Map** — Village cluster cards color-coded by status (🟢 SAFE / 🟡 WARNING / 🔴 CRITICAL), vital signs display
- **🚦 Traffic Light** — VLE trust score table with progress bars, verification history with variance/confidence details
- **📥 Data Export** — CSV download with data preview

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<p align="center">
  <strong>Built for India's villages. Powered by open-source.</strong><br/>
  <em>भारत-सेतु — bridging rural India to digital prosperity</em>
</p>
