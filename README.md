# Mayank7211 Portfolio

This repository now serves as a recruiter-friendly portfolio for the AI work you built in this workspace, centered on the AI Assistant Builder project.

## Featured work
- [PROJECTS_INDEX.md](PROJECTS_INDEX.md) - one-page index of the project and portfolio assets
- [PORTFOLIO_README.md](PORTFOLIO_README.md) - main public-facing GitHub profile summary
- [PROJECT_SHOWCASE.md](PROJECT_SHOWCASE.md) - technical deep-dive on the AI Assistant Builder
- [SKILLS_AND_EXPERIENCE.md](SKILLS_AND_EXPERIENCE.md) - ML, Python, FastAPI, and systems skills
- [RECRUITER_QUICKSTART.md](RECRUITER_QUICKSTART.md) - fast overview for hiring managers
- [GITHUB_UPLOAD_GUIDE.md](GITHUB_UPLOAD_GUIDE.md) - GitHub publishing steps

## Other projects to showcase
- [Mayank7211/Mayank7211](https://github.com/Mayank7211/Mayank7211) - GitHub profile repository and public entry point
- [Mayank7211/Mayank7211.github.io](https://github.com/Mayank7211/Mayank7211.github.io) - personal portfolio website on GitHub Pages
- [Mayank7211/Resturant-app](https://github.com/Mayank7211/Resturant-app) - full-stack restaurant ordering application
- [Mayank7211/ai-reel-automator](https://github.com/Mayank7211/ai-reel-automator) - AI-powered automation tool for reel creation

## Main project in this repo
- AI Assistant Builder for local businesses
- Multi-tenant backend API with FastAPI
- React + Vite onboarding and chat UI
- Model gateway abstraction with routing and fallback
- Postgres-backed persistence for tenants, knowledge, and conversations
- Docker compose stack for local development

## Project layout
- apps/backend: FastAPI API and assistant orchestration
- apps/frontend: React onboarding and chat testing UI
- infra/sql: database schema scripts
- widget: embeddable assistant widget assets

## Quick start with Docker
1. From workspace root run:
   - docker compose up --build
2. Open frontend at:
   - http://localhost:3000
3. Backend health:
   - http://localhost:8000/health

## Quick start without Docker
### Backend
1. Open terminal in apps/backend.
2. Create virtual environment and activate.
3. Install dependencies with pip install -r requirements.txt.
4. Set a local DB URL (example):
   - AI_AGENT_DATABASE_URL=sqlite+aiosqlite:///./sql_app.db
5. Run API:
   - uvicorn app.main:app --reload --port 8000

### Frontend
1. Open terminal in apps/frontend.
2. Install dependencies:
   - npm install
3. Run dev server:
   - npm run dev
4. Open local URL printed by Vite (default http://localhost:5173).

## Current MVP API
- GET /health
- POST /api/tenants
- POST /api/tenants/{tenant_id}/knowledge
- POST /api/chat

## Next production steps
- Add pgvector embeddings and semantic retrieval
- Add tenant auth, API keys, and strict rate limiting
- Add real model providers via environment-driven gateway
- Add conversation persistence and evaluation tests
- Add Cloudflare deployment and edge protections
