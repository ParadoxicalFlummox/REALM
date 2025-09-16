# TAPRE: Tracking & Analytics Platform for Real Estate

## Project Tech Stack Decision and Architecture Overview

### 1. Chosen Tech Stack

- **Frontend:** Vue.js  
  - Open source, community driven, approachable, and flexible.
- **Backend:** Go (Gin)  
  - Minimal, performant, just works.
- **Database:** PostgreSQL  
  - Robust, scalable, and ideal for structured data.
---

### 3. Typical App Architecture

```
User (Browser/App)
   |
   v
Frontend (Vue.js)
   |
   v
REST API (Go + Gin)
   |
   v
PostgreSQL Database
```

#### Example Workflow

- **User registers:** Vue.js app sends POST to `/api/signup`, Gin handles validation and writes to PostgreSQL.
- **User logs in:** Receives a JWT for future authenticated requests.
- **CRUD actions:** Vue.js calls REST endpoints for tasks, Gin talks to PostgreSQL.

---

### 4. Summary

- **Vue.js + Gin + PostgreSQL** is a highly open, flexible, and modern stack.
- Each layer is container-friendly and widely supported.

---

# TAPRE MVP Focus: Property Investment Tracker

TAPRE's initial release is focused on being a powerful investment tracker for rental properties. The goal is to help investors get a clear view of how their properties are performing, compare rents to the market, and receive actionable advice to optimize returns. Advanced features (valuation, component tracking, tax write-off advice, etc.) will be added as future upgrades.

### Core Features (Phase 1)
- **User Authentication:** Secure login and registration.
- **Property Management:** Add, edit, and remove rental properties.
- **Investment Tracking:** 
  - Track purchase price, mortgage, expenses, income, and cash flow for each property.
  - Calculate and display key metrics (ROI, cash-on-cash return, cap rate, etc.).
- **Performance Dashboard:** 
  - Visualize property performance over time.
  - Highlight underperforming properties.
- **Rent Comparison:** 
  - Compare user’s rent to market averages (via integration or manual input).
  - Provide suggestions for rent optimization.
- **Advice & Insights:** 
  - Show actionable tips to improve property performance (e.g., raise rent, reduce expenses).

### Future Add-ons (Phase 2+)
- **Valuation Tracking:** Automated or manual property value updates.
- **Component Tracking:** Track appliances, renovations, and their depreciation.
- **Tax Write-off Advice:** Personalized tax optimization tips.
- **Premium Analytics:** Advanced reporting, AI-driven insights, benchmarking.
- **Professional Advice:** Connect with experts for personalized recommendations.

TAPRE is an all-in-one real estate toolkit designed for small real estate investors and landlords. The mission is to maximize ROI, simplify operations, and empower users to grow their wealth with actionable insights, tax optimization, and seamless property management.

## Key Features

- **Real-Time Property Valuation & Predictive Analytics**: Instantly view up-to-date estimates of your property values and equity using integrated market data and predictive trends.
- **Component Age Tracking & Maintenance Alerts**: Monitor property components (e.g., roofs, HVAC) and receive proactive alerts to prevent costly repairs. Integrates with local service providers and smart home devices (planned).
- **Receipt & Expense Management with OCR & Tax Optimization**: Upload receipts, extract details automatically, and receive AI-driven tax deduction suggestions. Export reports and integrate with tax software (TurboTax, etc.).
- **Basic Listing Creation**: Quickly generate listing templates for platforms like Zillow and Craigslist. Advanced marketing integrations and tenant screening are deprioritized to focus on core value.
- **Rent Collection & Document Storage**: Collect rent online (Stripe/PayPal), store important documents, and receive renewal reminders. In-app messaging and maintenance request tracking are streamlined or linked to external tools.
- **AI-Driven Investment Insights**: Personalized analytics on portfolio performance, cash flow, and ROI, with actionable advice (e.g., refinance, buy/sell/hold recommendations).
- **Local Service Marketplace**: Connect with vetted local service providers for repairs and maintenance, earning discounts and streamlining property care (Pro tier).

## Target Users
- Small landlords and property owners (1–10 properties)
- Real estate investors seeking efficiency, cost savings, and wealth growth

## Planned Technology Stack
- **Frontend**: Vue.js
- **Backend**: Go (Gin)
- **Database**: PostgreSQL
- **Integrations**: Real estate APIs for valuation, accounting APIs, tax software, local service providers

## Roadmap
1. **MVP**: Core valuation, maintenance alerts, receipt/OCR, rent collection, document storage, basic listing
   - **Duration:** 6-8 weeks
2. **Deployment & Containerization**: Docker, Kubernetes manifests, cloud/self-hosting docs
   - **Duration:** 2 weeks
3. **Financial Optimization Tools**: Tax optimization, deduction suggestions, tax software integration, landlord tax guides
   - **Duration:** 2-3 weeks
4. **Mobile App**: React Native app for on-the-go management
   - **Duration:** 2-3 months
5. **AI-Driven Insights**: Portfolio analytics, ROI/cash flow advice, predictive trends, advanced analytics
   - **Duration:** 1-2 months
6. **Local Service Marketplace**: Provider listings, booking interface, commission system
   - **Duration:** 1-2 months

## Development Timeline & Person Hours

| Phase                                 | Estimated Hours | Estimated Duration |
|----------------------------------------|-----------------|-------------------|
| MVP (Core features)                    | 80              | 6-8 weeks         |
| Deployment & Containerization          | 20              | 2 weeks           |
| Financial Optimization Tools           | 40              | 2-3 weeks         |
| Mobile App (Core features)             | 60              | 2-3 months        |
| AI-Driven Insights                     | 40              | 1-2 months        |
| Local Service Marketplace              | 40              | 1-2 months        |
| **Total**                              | **280**         | **10-22 months**   |

> **Note:** These are rough estimates and actual time may vary based on feature complexity, learning curve, and unforeseen challenges. Timelines now assume part-time development (3-7 hours/week).

## Abbreviations & Meanings

- **MVP**: Minimum Viable Product – The simplest version of the software that delivers core value and is functional enough for real-world use.
- **CRUD**: Create, Read, Update, Delete – The four basic operations for managing data in an application.
- **REST API**: Representational State Transfer Application Programming Interface – A standard way for web applications to communicate with each other.
- **OCR**: Optical Character Recognition – Technology that converts different types of documents, such as scanned paper documents or images, into editable and searchable data.
- **K8s**: Kubernetes – An open-source platform for automating deployment, scaling, and management of containerized applications.
- **SaaS**: Software as a Service – A software distribution model in which applications are hosted by a service provider and made available to customers over the internet.
- **P&L**: Profit and Loss – A financial statement that summarizes revenues, costs, and expenses during a specific period.
- **DB**: Database – An organized collection of structured information or data, typically stored electronically.
- **API**: Application Programming Interface – A set of rules that allows different software entities to communicate with each other.
- **UI**: User Interface – The space where interactions between humans and machines occur.
- **FOSS**: Free and Open Source Software

## Getting Started
*Instructions for setup and contribution will be added as development begins.*

### Default Admin Credentials (First-Time Setup)

When you first run TAPRE, a default admin user is created for initial configuration:

- **Username:** admin
- **Password:** admin123
- **Email:** admin@example.com

> ⚠️ **Security Warning:**
> After your first login, you must change the default admin password and email to secure your installation. Leaving the default credentials unchanged is a serious security risk.

## Self-Hosting & Deployment

TAPRE is designed as a fully containerized solution. You can deploy and run TAPRE on your own hardware or cloud infrastructure for free, at your own risk. All core features are available for self-hosted users, and you retain full control over your data and environment.

- **Containerized Deployment:**
  - Docker and Kubernetes manifests will be provided for easy setup.
  - Documentation will guide you through installation, configuration, and updates.
  - Community support is available for troubleshooting and best practices.

## Optional Managed Hosting & Premium Insights

For users who prefer a hassle-free experience or want access to advanced features, TAPRE will offer an optional managed hosting service:

- **Managed Hosting:**
  - We handle deployment, security, backups, and updates.
  - Hosted in secure, scalable cloud environments.
- **Premium Insights & Services:**
  - Access to advanced AI-driven analytics, professional advice, and exclusive integrations.
  - Additional features may include tax optimization, market trend predictions, and expert support.

Self-hosted users are always free to migrate to managed hosting at any time, and vice versa.

## Development Plan

For a detailed, step-by-step development plan and technical roadmap, see the [DevPlan.md](DevPlan.md) document in this repository.

## License

This project is licensed under the GNU General Public License v3.0 (GPLv3). See the [LICENSE](LICENSE) file for details.

---

*TAPRE empowers small landlords and investors to manage, grow, and optimize their real estate portfolios with confidence.*

## The TAPRE Project is a community-driven effort. Contributions, feedback, and suggestions are welcome! Join us in building a powerful tool for real estate investors.
## Development & Contribution