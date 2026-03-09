# TAPRE: Tracking & Analytics Platform for Real Estate

TAPRE is a self-hosted, modular platform for small landlords to track property performance. To prevent scope creep, development follows a **Backend-First** approach: each module's API and logic must be 100% complete before the Frontend is touched.

## Tech Stack
- **Backend:** Python (FastAPI) + SQLModel
- **Database:** PostgreSQL
- **Frontend:** Vue.js
- **Deployment:** Docker Compose

---

## Development Roadmap
The MVP is limited strictly to these phases. **No integrations or AI features until these are finished.**

### Phase 1: Foundations & relational core
- [x] Establish SQLModel Schema
- [x] Create modular CRUD routers
- [x] Build basic property financial summaries

### Phase 2: Portfolio intelligence & reporting
- [ ] Global dashboard route
- [ ] Search & filter
- [ ] Export engine

### Phase 3: Frontend bridge
- [ ] Vite + Vue setup
- [ ] API consumption
- [ ] Interactive dashboard

## Post MVP Project Phases

### Phase 4: Operational automation
- [ ] Maintenance ledger
- [ ] Reminder system
- [ ] Document Association 

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