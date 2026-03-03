# TAPRE: Tracking & Analytics Platform for Real Estate

TAPRE is a self-hosted, modular platform for small landlords to track property performance. To prevent scope creep, development follows a **Backend-First** approach: each module's API and logic must be 100% complete before the Frontend is touched.

## Tech Stack
- **Backend:** Python (FastAPI) + SQLModel
- **Database:** PostgreSQL
- **Frontend:** Vue.js
- **Deployment:** Docker Compose

---

## MVP Focus (The "Base" Project)
The MVP is limited strictly to these three modules. **No integrations or AI features until these are finished.**

1.  **Properties Module:** Core entity management (Address, Purchase Price, SqFt).
2.  **Ledger Module:** Financial tracking (Income, Expenses, Cash Flow).
3.  **Asset Module:** Property inventory (Appliances, HVAC, Roof age).

---

## Project Structure
Following the host-admin convention:
```./app/tapre/
├── docker-compose.yml
├── backend/            # FastAPI Modular Logic
│   └── modules/        # [properties, ledger, assets]
├── frontend/           # Vue.js (Phase 2)
├── config/             # App & DB configs
└── data/               # Persistent Postgres & Media volumes
```

## Project docker-compose.yml