# TAPRE: Tracking & Analytics Platform for Real Estate

TAPRE is a self-hosted, modular platform for real estate investors to track property performance and make better investment decisions. Development follows a **Backend-First** approach: each module's API and logic is completed before the frontend is built.

## Tech Stack
- **Backend:** Python (FastAPI) + SQLModel
- **Database:** PostgreSQL 18
- **Frontend:** Vue.js 3 (Composition API) + Tailwind CSS v4
- **Deployment:** Docker Compose

---

## Development Roadmap

### Phase 1: Foundations & Relational Core
- [x] SQLModel schema — Property, Transaction, Asset models
- [x] Modular CRUD routers
- [x] Relational integrity and cascade protection

### Phase 2: Portfolio Intelligence & Reporting
- [x] Per-property financial insights (cash flow, expense ratio, ROI)
- [x] Expense distribution by category
- [x] Rent target calculator (break-even and profit-target)

### Phase 3: Frontend
- [x] Vite + Vue 3 scaffold with Tailwind CSS v4
- [x] Properties list, detail view, and insights view
- [x] Transaction and asset management
- [x] Dark mode with localStorage persistence
- [x] Company name branding via environment variable

### Phase 4: Deal Analyzer
- [x] Pre-purchase and property-linked deal analysis
- [x] Full amortization math — mortgage, NOI, cash flow, DSCR, cash-on-cash return, break-even occupancy
- [x] Annual property tax estimate
- [x] Save analyses as snapshots — multiple scenarios per property
- [x] Schedule E tax categories on transactions (for future tax reporting)

### Phase 5: Equity & Debt Tracking
- [ ] Loan model per property — balance, rate, term, origination date
- [ ] Principal paydown tracking over time
- [ ] Equity, LTV, and estimated value per property

### Phase 6: Tax Reporting
- [ ] Schedule E export by tax year and property
- [ ] Depreciation estimate (purchase price ÷ 27.5 years)
- [ ] Tax summary from deal analyzer snapshots
- [ ] CSV / JSON export for accountant handoff

### Phase 7: Operational Automation
- [ ] Maintenance ledger
- [ ] Reminder system
- [ ] Document association

### Phase 8: Scenario Tools
- [ ] Refi / HELOC / portfolio loan scenario modeling
- [ ] What-if engine for refinance, cash-out, and portfolio roll-up
- [ ] Side-by-side scenario comparison

---

## Project Structure

```
TAPRE/
├── docker-compose.yml
├── .env                        # DB credentials and config (not committed)
├── .env.example                # Template for new deployments
├── backend/
│   ├── main.py                 # FastAPI app, CORS, router registration
│   ├── models.py               # SQLModel schema — Property, Transaction, Asset, Deal
│   ├── database.py             # Engine, session, init_db
│   ├── requirements.txt
│   ├── routes/
│   │   ├── properties.py
│   │   ├── transactions.py     # Includes Schedule E tax category endpoint
│   │   ├── assets.py
│   │   ├── dashboard.py        # Per-property financial insights
│   │   └── deals.py            # Deal analyzer — calculate + CRUD
│   └── services/
│       ├── dashboard_logic.py  # Financial metrics service
│       └── deal_logic.py       # Amortization and deal math service
└── frontend/
    ├── src/
    │   ├── api/                # Axios wrappers — one file per resource
    │   ├── views/              # Full-page components (one per route)
    │   ├── components/         # Reusable UI components
    │   └── router/             # Vue Router config
    ├── .env                    # VITE_COMPANY_NAME (not committed)
    └── .env.example
```

## Running Locally

**1. Start the database:**
```bash
docker compose up -d
```

**2. Start the backend:**
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

**3. Start the frontend:**
```bash
cd frontend
npm run dev
```

- Frontend: `http://localhost:5173`
- API docs: `http://localhost:8000/docs`
