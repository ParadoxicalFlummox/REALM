# TAP·re: Tracking & Analytics Platform for Real Estate

TAP·re is a self-hosted, open-source platform for real estate investors to track property performance and make better investment decisions. Licensed under **AGPL-3.0** — free to use, free to self-host, forever.

Development follows a **backend-first** approach: each module's data model and API are completed before the frontend is built.

## Tech Stack
- **Backend:** Python (FastAPI) + SQLModel
- **Database:** PostgreSQL 18
- **Frontend:** Vue.js 3 (Composition API) + Tailwind CSS v4
- **Deployment:** Docker Compose

---

## Development Roadmap

### Phase 1: Foundations & Relational Core ✅
- [x] SQLModel schema — Property, Transaction, Asset models
- [x] Modular CRUD routers with relational integrity
- [x] Cascade protection on deletes

### Phase 2: Portfolio Intelligence & Reporting ✅
- [x] Per-property financial insights (cash flow, expense ratio, ROI)
- [x] Expense distribution by category
- [x] Rent target calculator (break-even and profit-target)

### Phase 3: Frontend ✅
- [x] Vite + Vue 3 scaffold with Tailwind CSS v4
- [x] Properties list, detail view, and insights view
- [x] Transaction and asset management with inline editing
- [x] Dark mode with localStorage persistence
- [x] Company name branding via environment variable or in-app settings

### Phase 4: Deal Analyzer ✅
- [x] Pre-purchase and property-linked deal analysis
- [x] Full amortization math — mortgage, NOI, cash flow, DSCR, cash-on-cash return, break-even occupancy
- [x] Cash flow derivation breakdown for transparency
- [x] Annual property tax estimate
- [x] Save analyses as snapshots — multiple scenarios per property
- [x] Schedule E tax categories on transactions (groundwork for Phase 8)

### Phase 5: Equity & Debt Tracking ✅
- [x] Loan model per property — balance, rate, term, origination date
- [x] Amortization-based balance calculation (auto paydown tracking)
- [x] Manual balance override for real statement values
- [x] Equity, LTV, and estimated value per property

### Phase 6: Portfolio Dashboard ✅
- [x] Single-view portfolio overview across all properties
- [x] Aggregate equity, loan balance, and LTV
- [x] Per-property equity breakdown table
- [x] Company name links to portfolio; Properties nav is its own route

### Phase 7: Maintenance Ledger ✅
- [x] Maintenance record model — vendor, cost, date, linked asset/property
- [x] Maintenance log view per property with inline editing
- [x] Foundation schema for reminders (model only, no UI)
- [x] Foundation schema for document association (model only, no UI)

### Phase 8: Tax Reporting *(post v1.0)*
- [ ] Schedule E export by tax year and property
- [ ] Depreciation estimate (purchase price ÷ 27.5 years)
- [ ] Tax summary from deal analyzer snapshots
- [ ] CSV / JSON export for accountant handoff

### Phase 9: Scenario Tools *(post v1.0)*
- [ ] Refi / HELOC / portfolio loan scenario modeling
- [ ] What-if engine for refinance, cash-out, and portfolio roll-up
- [ ] Side-by-side scenario comparison

---

## Project Structure

```
TAP·re/
├── docker-compose.yml
├── .env                        # DB credentials and config (not committed)
├── .env.example                # Template for new deployments
├── backend/
│   ├── Dockerfile
│   ├── main.py                 # FastAPI app, CORS, router registration
│   ├── models.py               # SQLModel schema — all models
│   ├── database.py             # Engine, session, init_db
│   ├── requirements.txt
│   ├── routes/
│   │   ├── properties.py
│   │   ├── transactions.py     # Includes Schedule E tax category endpoint
│   │   ├── assets.py
│   │   ├── dashboard.py        # Per-property financial insights
│   │   ├── deals.py            # Deal analyzer — calculate + CRUD
│   │   ├── loans.py            # Loan CRUD + equity endpoint
│   │   ├── portfolio.py        # Portfolio-level summary
│   │   └── maintenance.py      # Maintenance ledger CRUD
│   └── services/
│       ├── dashboard_logic.py  # Financial metrics service
│       ├── deal_logic.py       # Amortization and deal math service
│       └── loan_logic.py       # Loan balance calculation service
└── frontend/
    ├── Dockerfile
    ├── nginx.conf              # Serves SPA + proxies /api/ to backend
    ├── src/
    │   ├── api/                # Axios wrappers — one file per resource
    │   ├── views/              # Full-page components (one per route)
    │   │   ├── PortfolioView.vue
    │   │   ├── PropertiesView.vue
    │   │   ├── PropertyDetailView.vue
    │   │   ├── InsightsView.vue
    │   │   └── DealAnalyzerView.vue
    │   ├── components/         # Reusable UI components
    │   └── router/             # Vue Router config
    └── vite.config.js          # envDir points to repo root for single .env
```

---

## Running Locally

**1. Copy and configure environment:**
```bash
cp .env.example .env
# Edit .env — set DB credentials, keep DATABASE_URL host as "localhost" for local dev
```

**2. Start the database:**
```bash
docker compose up db -d
```

**3. Start the backend:**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**4. Start the frontend:**
```bash
cd frontend
npm install
npm run dev
```

- Frontend: `http://localhost:5173`
- API docs: `http://localhost:8000/docs`

---

## Self-Hosting with Docker

**1. Copy and configure environment:**
```bash
cp .env.example .env
# Edit .env — set DB credentials, set DATABASE_URL host to "db" for Docker
```

**2. Build and run:**
```bash
docker compose up --build -d
```

Open `http://localhost` (or your server's IP).

**To deploy a pre-built release** (no source needed on the server):
```bash
# On the server — only needs docker-compose.yml + .env
docker compose pull
docker compose up -d
```

---

## License

TAP·re is licensed under the [GNU Affero General Public License v3.0](LICENSE).  
You are free to use, self-host, and modify TAP·re. Any modifications distributed or run as a network service must also be released under AGPL-3.0.
