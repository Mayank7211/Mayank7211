# 🚀 Quick Start Guide for Recruiters

> **In 5 minutes, understand the AI Assistant Builder architecture and capabilities**

---

## 📂 Repository Structure

```
📦 AI Assistant Builder
├── 📄 PORTFOLIO_README.md          👈 START HERE (Your main profile)
├── 📄 PROJECT_SHOWCASE.md          👈 Project deep-dive
├── 📄 SKILLS_AND_EXPERIENCE.md     👈 ML/Backend skills breakdown
│
├── 📁 apps/backend/                Flask/FastAPI Backend
│   ├── 📁 app/
│   │   ├── main.py                 Route setup
│   │   ├── 📁 api/
│   │   │   ├── chat.py             Chat endpoint (LLM routing)
│   │   │   ├── analytics.py        Real-time metrics (6 endpoints)
│   │   │   └── tenants.py          Business profile + file upload
│   │   ├── 📁 services/
│   │   │   ├── assistant_service.py   LLM integration + prompt
│   │   │   ├── document_parser.py     PDF/DOCX/TXT processing
│   │   │   ├── model_gateway.py       Multi-model routing
│   │   │   ├── analytics.py           Metrics collection
│   │   │   └── knowledge.py           Document retrieval
│   │   ├── 📁 core/
│   │   │   ├── config.py           Environment & settings
│   │   │   ├── database.py         Async SQLAlchemy + multi-tenant
│   │   │   ├── rate_limits.py      Tenant-based throttling
│   │   │   └── auth/dependencies.py Auth middleware
│   │   ├── 📁 models/
│   │   │   ├── entities.py         SQLAlchemy ORM models
│   │   │   ├── schemas.py          Pydantic request/response
│   │   │   └── tenant.py           Tenant entity
│   │   └── routes/                 API route handlers
│   │
│   ├── requirements.txt            Python dependencies
│   ├── Dockerfile                  Container setup
│   ├── test_api.py                Test endpoints manually
│   └── tests/
│       ├── test_health.py
│       ├── test_tenant_authz.py    Multi-tenant isolation tests
│       ├── test_rate_limits.py
│       └── test_upload_api.py      Document upload validation
│
├── 📁 apps/frontend/               React + Vite Admin Dashboard
│   ├── src/
│   │   ├── App.tsx                 Main component
│   │   ├── main.tsx                Entry point
│   │   ├── 📁 components/
│   │   │   ├── AdminDashboard.tsx 👈 Analytics dashboard (key file)
│   │   │   ├── ChatSandbox.tsx      Chat testing UI
│   │   │   └── OnboardingForm.tsx   Business profile form
│   │   └── 📁 lib/
│   │       ├── api.ts              Backend API client
│   │       └── utils.ts            Helper functions
│   ├── package.json                Node dependencies
│   ├── tsconfig.json               TypeScript config
│   ├── vite.config.ts              Build config
│   └── Dockerfile                  Container setup
│
├── 📁 widget/                      Embeddable JavaScript Widget
│   ├── agent.js                    👈 15KB vanilla JS (key file)
│   └── index.html                  Widget standalone demo
│
├── 📁 infra/sql/
│   └── 001_init.sql               PostgreSQL schema
│
├── docker-compose.yml              Full stack local dev setup
├── README.md                       Basic setup
└── GOAL-AND-IMPROVEMENTS.md       Original vision document
```

---

## 🎯 5-Minute Deep Dive

### 1. **What Did You Build?** (1 min)
📖 Read: `PROJECT_SHOWCASE.md` → "Project Overview" section
- ✅ Multi-tenant AI assistant platform
- ✅ Free-tier LLM (Groq API)
- ✅ Document intelligence (PDF/DOCX/TXT)
- ✅ Embeddable widget for any website
- ✅ React admin dashboard with analytics

### 2. **Backend Architecture** (2 min)
📖 Read: `apps/backend/app/` structure

**Key Files**:
- `main.py` - FastAPI app setup, route mounting
- `core/database.py` - Async SQLAlchemy ORM, multi-tenant design
- `services/assistant_service.py` - LLM integration logic
- `services/document_parser.py` - PDF/DOCX parsing
- `api/analytics.py` - Real-time metrics endpoints

**Key Concepts**:
```python
# Multi-tenant: All requests filtered by tenant_id
@app.post("/api/chat")
async def chat(req: ChatRequest, tenant_id: str) -> ChatResponse:
    # Load business context
    # Route to appropriate LLM model
    # Track metrics
    # Return response with confidence score
```

### 3. **ML/AI Capabilities** (1.5 min)
📖 Read: `SKILLS_AND_EXPERIENCE.md` → "Core Competencies"

**ML Systems Built**:
- ✅ LLM routing (cost vs. quality tradeoff)
- ✅ Document parsing & chunking
- ✅ Prompt engineering (domain-specific)
- ✅ Conversation memory
- ✅ Reservation detection (NLP)
- ✅ Confidence scoring & monitoring

### 4. **Frontend & Widget** (0.5 min)
📖 Brief look:
- `widgets/agent.js` - Embeddable chat widget (15KB, no deps)
- `apps/frontend/src/components/AdminDashboard.tsx` - 3-tab analytics dashboard
- **Responsive**: Mobile full-screen, desktop floating window

---

## 🔍 Key Files for Different Reviewers

### For Backend/Systems Engineers
```
Priority 1: apps/backend/app/core/database.py
            → Multi-tenant design, async SQLAlchemy

Priority 2: apps/backend/app/main.py
            → API structure, dependency injection

Priority 3: apps/backend/app/services/assistant_service.py
            → LLM integration pattern

Priority 4: apps/backend/tests/test_tenant_authz.py
            → Security & isolation verification
```

### For ML/AI Engineers
```
Priority 1: apps/backend/app/services/document_parser.py
            → Document intelligence pipeline

Priority 2: apps/backend/app/services/assistant_service.py
            → LLM integration, prompt engineering

Priority 3: apps/backend/app/api/analytics.py
            → ML monitoring & metrics

Priority 4: SKILLS_AND_EXPERIENCE.md
            → ML concepts applied
```

### For Full-Stack/Frontend Engineers
```
Priority 1: apps/frontend/src/components/AdminDashboard.tsx
            → React real-time dashboard

Priority 2: widget/agent.js
            → Embeddable vanilla JS widget

Priority 3: apps/frontend/src/lib/api.ts
            → Backend API client
```

### For Product/Founder Perspective
```
Priority 1: PROJECT_SHOWCASE.md → "Project Overview"
Priority 2: PORTFOLIO_README.md → "Key Achievements"
Priority 3: docker-compose.yml → All-in-one setup
Priority 4: README.md → Quick start
```

---

## 🚀 Run It Locally (3 commands)

```bash
# Clone and enter workspace
git clone https://github.com/Mayank7211/Mayank7211.git
cd Mayank7211

# Start everything (backend, frontend, database)
docker compose up --build

# Open in browser
http://localhost:3000   # Frontend + Dashboard
http://localhost:8000/docs  # Backend API docs (Swagger)
```

**Without Docker**:
```bash
# Backend
cd apps/backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd apps/frontend
npm install
npm run dev
```

---

## 📊 System Metrics Snapshot

| Metric | Value | What It Shows |
|--------|-------|--------------|
| **Deployment Time** | < 30 min | Product velocity |
| **Cost per Business** | ~$0 | Affordability |
| **API Endpoints** | 10 | Full-featured |
| **Analytics Tracks** | 6 systems | Comprehensive monitoring |
| **Widget Size** | 15KB | Performance-optimized |
| **Database Queries** | Async/pooled | Scalability |

---

## 🎓 What This Demonstrates

### Technical Skills
✅ Full-stack development (backend + frontend + DevOps)
✅ Production system design
✅ LLM integration in real application
✅ Multi-tenant architecture
✅ Async Python best practices
✅ Docker containerization
✅ REST API design
✅ React component development

### Soft Skills
✅ Problem-solving (cost optimization, reliability)
✅ End-to-end responsibility
✅ Attention to production requirements
✅ Code organization & maintainability
✅ Self-directed learning

---

## 💬 Conversation Starters

**"Tell me about your most complex project"**
→ This AI Assistant Builder: Multi-tenant system, LLM integration, full-stack

**"How do you optimize for cost?"**
→ Free-tier Groq API, multi-model routing strategy, fallback mechanisms

**"What's your experience with LLMs?"**
→ Integrated Groq API; prompt engineering for domain tasks; confidence tracking; multi-model routing

**"Describe your backend expertise"**
→ FastAPI, async SQLAlchemy, multi-tenant design, rate limiting, CORS

**"How do you approach production systems?"**
→ Error handling, monitoring, security (tenant isolation), performance optimization

---

## 📚 Recommended Reading Order

1. **First**: `PORTFOLIO_README.md` - Overview + skills
2. **Second**: `PROJECT_SHOWCASE.md` - Architecture deep-dive
3. **Third**: `SKILLS_AND_EXPERIENCE.md` - ML/Tech breakdown
4. **Then**: Explore specific code files based on role interest
5. **Finally**: Clone & run locally to see it working

---

## ✅ Verification Checklist

Use this to verify you're looking at everything:

- [ ] Read PORTFOLIO_README.md (main profile)
- [ ] Read PROJECT_SHOWCASE.md (project details)
- [ ] Read SKILLS_AND_EXPERIENCE.md (skills alignment)
- [ ] Reviewed backend architecture (apps/backend/app/)
- [ ] Reviewed frontend dashboard (apps/frontend/src/components/)
- [ ] Explored widget code (widget/agent.js)
- [ ] Checked database schema (infra/sql/001_init.sql)
- [ ] Ran `docker compose up` locally
- [ ] Accessed http://localhost:3000 (frontend)
- [ ] Accessed http://localhost:8000/docs (API docs)

---

## 🎯 Recruiter Quick Facts

- **Role Targeted**: ML Engineer / Backend Engineer / AI Systems Engineer
- **Key Project**: Full-stack AI Assistant Builder (production-ready)
- **Tech Stack**: Python (FastAPI) | React | PostgreSQL | LLMs | Docker
- **ML Skills**: LLM integration, prompt engineering, document parsing, model routing
- **Standout**: Built complete system from scratch (design → code → deployment)

---

**Questions?** Feel free to reach out. I'm happy to discuss architecture, design decisions, or live demo any component.

