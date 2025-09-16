# TAPRE MVP Checklist

This document converts the in-repo todo list into an expanded, ordered checklist with task descriptions, acceptance criteria, estimated effort, and the files likely affected. Use this as a roadmap to build your MVP.

> Note: The project README and DevPlan indicate the MVP is a Property Investment Tracker with core features: auth, property CRUD, investment tracking, dashboard, and rent comparison.

---

## 1) Fix initializers & main DONE
- Purpose: Ensure the application can build and connect to the database.
- Subtasks:
  - Fix package name typo `initalizers` → `initializers` in `backend/initializers/*.go`.
  - Add missing imports (`os`, `log`) and use them appropriately.
  - Assign the opened gorm DB to `initializers.DB`.
  - Update `main.go` imports to reference the module path from `go.mod` and remove stray imports.
  - Make sure `main()` calls the migration runner after DB connect.
- Files affected: `backend/main.go`, `backend/initializers/database.go`, `backend/initializers/loadEnvVariables.go`.
- Acceptance criteria: `go build ./...` completes; running `go run .` logs DB connection success or a clear error.
- Estimate: 1–2 hours.


## 2) Fix model definitions DONE
- Purpose: Ensure models are usable by GORM and JSON serialization.
- Subtasks:
  - Export model types and fields (capitalize names).
  - Correct `time.Time` types and add `CreatedAt`/`UpdatedAt` or embed `gorm.Model`.
  - Add `gorm` tags and `json` tags for important fields.
  - Rename or export types so relationships work (e.g., `FinancialRecord` not `financialRecord`).
- Files affected: `backend/models/*.go` (`user.go`, `property.go`, `financial_record.go`).
- Acceptance criteria: `go build` passes and GORM AutoMigrate can accept the model types.
- Estimate: 1–3 hours.


## 3) Add migration runner DONE
- Purpose: Automatically create the necessary tables in the database during startup (dev convenience).
- Subtasks:
  - Implement `backend/migrate/migrate.go` with `RunMigrations()` calling `initializers.DB.AutoMigrate(&models.User{}, &models.Property{}, &models.FinancialRecord{})`.
  - Call `migrate.RunMigrations()` from `main()` after `ConnectToDB()`.
- Files affected: `backend/migrate/migrate.go`, `backend/main.go`.
- Acceptance criteria: Starting the app creates/updates DB tables without errors.
- Estimate: 30–60 minutes.


## 4) Seed default admin & env docs DONE
- Purpose: Provide a default admin for initial setup and document environment variables.
- Subtasks:
  - Add `.env.example` with `DB_CREDS`, `JWT_SECRET`, and other variables.
  - Implement an idempotent seeder to create a default admin (configurable by env) during startup.
  - Document the seeder and env vars in `README.md`.
- Files affected: `backend/migrate/*` or `backend/initializers/*`, `README.md`, `.env.example`.
- Acceptance criteria: After startup, admin user exists and credentials are documented.
- Estimate: 1–2 hours.


## 5) Implement repositories/services (CRUD)
- Purpose: Separate DB access from handlers for testability and clear layering.
- Subtasks:
  - Create `backend/repositories` package with `user_repo.go`, `property_repo.go`, `financial_repo.go`.
  - Implement standard CRUD functions returning domain errors.
  - Add unit tests for repository functions (mock DB with SQLite or test DB).
- Files affected: `backend/repositories/*`, model files for types.
- Acceptance criteria: Repositories compile and pass unit tests.
- Estimate: 4–8 hours.


## 6) Implement JWT auth
- Purpose: Secure endpoints and provide session management.
- Subtasks:
  - Add `handlers/auth.go` with signup/login endpoints.
  - Hash passwords with `bcrypt` before storing.
  - Generate signed JWTs using `JWT_SECRET` environment variable.
  - Add middleware `middleware/auth.go` to enforce auth and attach `User` to the context.
- Files affected: `backend/handlers/auth.go`, `backend/middleware/auth.go`, `go.mod` (add jwt library), `README.md`.
- Acceptance criteria: Able to register/login and obtain a JWT; protected endpoints return 401 without a valid token.
- Estimate: 4–8 hours.


## 7) Property CRUD API
- Purpose: Allow owners to manage properties via REST.
- Subtasks:
  - Add `handlers/property.go` with create/read/update/delete handlers.
  - Validate ownership for write operations.
  - Wire routes in `main.go` under `/api/v1/properties`.
- Files affected: `backend/handlers/property.go`, `backend/main.go`.
- Acceptance criteria: CRUD endpoints work end-to-end with JWT auth.
- Estimate: 4–8 hours.


## 8) Financial records CRUD + metrics
- Purpose: Track incomes and expenses and compute investment metrics.
- Subtasks:
  - Add `handlers/financial.go` for adding/listing records.
  - Implement services to compute ROI, cash-on-cash, cap rate per property.
  - Add endpoints for summarized metrics per property.
- Files affected: `backend/handlers/financial.go`, `backend/services/metrics.go`.
- Acceptance criteria: Can add records and retrieve correct basic metrics.
- Estimate: 6–12 hours (depends on metric complexity).


## 9) Add Gin routers & route groups
- Purpose: Organize routes and middleware consistently.
- Subtasks:
  - Create route groups `/api/v1/auth`, `/api/v1/users`, `/api/v1/properties`, `/api/v1/records`, `/api/v1/dashboard`.
  - Register middlewares: logging, CORS, auth, recovery.
- Files affected: `backend/main.go`, `backend/middleware/*`.
- Acceptance criteria: API grouped and middleware applied as expected.
- Estimate: 1–2 hours.


## 10) Frontend skeleton (Vue) & API client
- Purpose: Provide a UI to interact with the API for MVP flows.
- Subtasks:
  - Create a minimal Vue app (or static HTML) with pages for login, property list, property detail, and add property.
  - Build a small API client (Axios) and map endpoints.
  - Option: Add the built assets to `backend/public` and serve as static files.
- Files affected: `web/` or `frontend/` folder, `backend/main.go` (serve static files).
- Acceptance criteria: Basic UI able to login and list properties.
- Estimate: 8–16 hours.


## 11) Dashboard endpoints & basic charts
- Purpose: Return time-series and summary data for charts in the frontend.
- Subtasks:
  - Implement endpoints to return monthly cashflow, income vs expenses, and property snapshot.
  - Use charting library in the frontend (Chart.js, ECharts) to visualize data.
- Files affected: `backend/handlers/dashboard.go`, frontend chart components.
- Acceptance criteria: Frontend shows charts populated with API data.
- Estimate: 6–12 hours.


## 12) Rent comparison (MVP manual)
- Purpose: Provide basic rent comparison capabilities without external APIs.
- Subtasks:
  - Allow manual input of market rent for a property and store it.
  - Provide a comparison endpoint that returns a delta and suggestion.
- Files affected: handler updates and frontend form.
- Acceptance criteria: Manual rent comparison returns sensible output.
- Estimate: 2–4 hours.


## 13) Advice & insights prototype
- Purpose: Provide actionable tips to improve ROI for a property.
- Subtasks:
  - Implement a simple rule-based engine (if cash-on-cash < X, suggest actions).
  - Return advice via an endpoint and display in frontend.
- Files affected: `backend/services/advice.go`, frontend UI.
- Acceptance criteria: Advice engine returns deterministic suggestions based on metrics.
- Estimate: 4–8 hours.


## 14) Testing & smoke tests
- Purpose: Ensure core flows work and regressions are caught early.
- Subtasks:
  - Add unit tests for repositories and handlers.
  - Add an integration smoke test script that runs against a test DB (or uses Docker Compose to spin up PostgreSQL).
- Files affected: `backend/*_test.go`, `scripts/smoke_test.sh` or a Go test package.
- Acceptance criteria: `go test ./...` passes for core packages; smoke test completes.
- Estimate: 6–12 hours.


## 15) Dockerize & docker-compose
- Purpose: Make local development and deployment repeatable.
- Subtasks:
  - Add a multi-stage `Dockerfile` for the backend.
  - Update `deploy/docker-compose.yml` to include `app` and `postgres` services and env var references.
  - Add `.env.example` and instructions in README.
- Files affected: `backend/Dockerfile`, `deploy/docker-compose.yml`, `.env.example`.
- Acceptance criteria: `docker-compose up` starts both containers and app connects to DB.
- Estimate: 3–6 hours.


## 16) CI pipeline (GitHub Actions)
- Purpose: Run tests and linting on every push/PR.
- Subtasks:
  - Add `.github/workflows/ci.yml` to run `go test ./...`, `go vet`, and optionally linters.
  - Add a build job to build the Docker image (or at least `go build`).
- Files affected: `.github/workflows/*`.
- Acceptance criteria: Pull requests trigger CI and tests run.
- Estimate: 2–6 hours.


## 17) Docs & README completion
- Purpose: Make it easy for contributors and self-hosters to get started.
- Subtasks:
  - Document env vars, run steps, seeding, and Docker/Compose usage.
  - Add API contract examples for key endpoints.
- Files affected: `README.md`, `DevPlan.md`, `docs/` (optional), `.env.example`.
- Acceptance criteria: New contributor can follow docs to run the app locally.
- Estimate: 2–6 hours.


## 18) Phase 2 features & epics (future)
- Purpose: Track larger features for later implementation (valuation, OCR, mobile app, AI insights).
- Subtasks: Create epics/tickets for each feature and prioritize them after the MVP.
- Files affected: project management only (issues, milestones).
- Acceptance criteria: Clear backlog and priorities.
- Estimate: ongoing.

---

# Prioritization & Sprinting advice
- Sprint 0 (Setup, 1 week): Items 1–4 (DB connect, models, migration, seed admin), plus create `.env.example` and basic README updates.
- Sprint 1 (Core API, 2–3 weeks): Items 5–9 (repositories, auth, property CRUD, financial records, routers).
- Sprint 2 (Frontend MVP, 2–3 weeks): Items 10–13 (Vue skeleton, dashboard, rent comparison, advice prototype).
- Sprint 3 (Stabilize & Ship, 1 week): Items 14–17 (tests, Docker Compose, CI, docs).

# Acceptance checklist for MVP
- User can register and log in (JWT issued)
- User can create/edit/delete properties they own
- User can log incomes/expenses per property
- Dashboard shows cashflow metrics and simple charts
- App runs locally via `docker-compose up` with a Postgres DB
