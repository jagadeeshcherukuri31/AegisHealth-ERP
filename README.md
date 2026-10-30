# AegisHealth ERP

Hospital ERP covering patients, appointments, electronic health records, billing, pharmacy inventory and staff.
Flask + SQLAlchemy + JWT backend, plain HTML/CSS/JS frontend.

## Run it

```bash
# 1. Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py                # http://localhost:5000, creates SQLite tables

# 2. Optional demo data (loads accounts, patients, appointments, stock)
python - <<'PY'
import sqlite3
c = sqlite3.connect("instance/aegis.db")   # path may be backend/aegis.db depending on Flask version
c.executescript(open("../database/seed.sql").read()); c.commit()
PY

# 3. Frontend (separate terminal)
cd frontend && python -m http.server 8080   # open http://localhost:8080
```

Demo login: `admin@aegis.test` / `Aegis@123` (also `doctor@`, `nurse@`, `reception@`, `pharmacy@`, `billing@`).

To use a different API URL, set `window.API_BASE` before `api.js` loads.

## Tests

```bash
cd backend && pytest
```

## Roles

| Role | Access |
|---|---|
| admin | everything, plus user creation |
| doctor | patients, appointments, write medical records, view pharmacy |
| nurse | patients, appointments, read records, view pharmacy |
| receptionist | patients, appointments, billing |
| pharmacist | pharmacy (dispense, restock), patient lookup |
| billing | invoices and payments, patient lookup |

## Layout

See `docs/architecture.md` and `docs/api-documentation.md`.

## Before production

Change both secrets in `.env`, restrict CORS origins in `app/extensions.py`, serve over HTTPS, and keep the JWT in an
httpOnly cookie instead of localStorage. Patient data is regulated (HIPAA/GDPR); this project is a starting point, not a compliant system.
