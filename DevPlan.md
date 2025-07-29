# TAPRE Requirements & MVP Focus

## MVP: Property Investment Tracker

### Core Features (Phase 1)
- **User Authentication:** Secure login and registration.
  - Uses JWT authentication.
- **Property Management:** Add, edit, and remove rental properties.
  - CRUD operations for properties with details like address, purchase price, mortgage info, etc.
- **Investment Tracking:** 
  - Track purchase price, mortgage, expenses, income, and cash flow for each property.
  - Calculate and display key metrics (ROI, cash-on-cash return, cap rate, etc.).
- **Performance Dashboard:** 
  - Visualize property performance over time.
  - Highlight underperforming properties.
- **Rent Comparison:** 
  - Compare user’s rent to market averages (via integration or manual input).
  - Provide suggestions for rent optimization.
  - Calculate profit margin and compare it to market standards.
- **Advice & Insights:** 
  - Show actionable tips to improve property performance (e.g., raise rent, reduce expenses).

### Future Add-ons (Phase 2+)
- **Valuation Tracking:** Automated or manual property value updates.
- **Component Tracking:** Track appliances, renovations, and their depreciation.
- **Tax Write-off Advice:** Personalized tax optimization tips.

---

# TAPRE Development Plan & Timeline

## 1. Project Architecture & Planning 
- Define core components: frontend (Vue.js), backend (Go/Gin), database (PostgreSQL), and optional services (AI microservices).
- Establish API contracts and data models.
- Set up version control and branching strategy (main, dev, feature branches).

**Duration:** 1 week

---

## 2. MVP Implementation
- Develop core features: authentication, property management, investment tracking, dashboard, rent comparison, advice/insights.
- Build RESTful API endpoints in Go (Gin).
- Build Vue.js UI for all MVP features.
- Integrate frontend and backend.
- Write unit and integration tests.

**Duration:** 6-8 weeks

---

## 3. Deployment & Containerization
- Write Dockerfiles for each component:
  - Frontend: Build and serve with Nginx.
  - Backend: Go (Gin) app.
  - Database: Use official PostgreSQL image.
- Test each container independently.
- Create a `docker-compose.yml` to orchestrate all services.
- Set up environment variables and secrets for local development.
- Test the full stack locally: frontend ↔ backend ↔ database.

**Duration:** 2 weeks

---

## 4. Financial Optimization Tools
- Implement tax optimization, deduction suggestions, and tax software integration.
- Add landlord tax guides and related UI/UX.

**Duration:** 2-3 weeks

---

## 5. Mobile App
- Develop a React Native app for on-the-go management.
- Integrate with backend REST API.
- Focus on core features: property management, notifications, and dashboard.

**Duration:** 2-3 months

---

## 6. AI-Driven Insights
- Add advanced analytics, portfolio optimization, and predictive trends.
- Provide actionable advice (e.g., refinance, buy/sell/hold recommendations).

**Duration:** 1-2 months

---

## Total Estimated Timeline
**10-22 months** (part-time development, 3-7 hours/week)
