# Mayank Aura

> ML Engineer portfolio, AI systems work, and public project showcase.

This repository is the public-facing home for my work and the place I want to share with recruiters, collaborators, and anyone curious about what I build.

## Live site

- Domain: [mayankaura.me](https://mayankaura.me)
- Portfolio target: a polished, interactive public site with custom branding, project cards, and clear contact paths
- Hosting direction: free static hosting for the frontend, with optional API hosting if the site needs live backend features

## Featured projects

### 1. [Mayank7211](https://github.com/Mayank7211/Mayank7211)
My GitHub profile repository and personal landing page.

What it shows:
- Personal brand and public entry point
- Recruiter-facing summary of my strongest work
- A clean overview of skills, projects, and interests

### 2. [Mayank7211.github.io](https://github.com/Mayank7211/Mayank7211.github.io)
My portfolio website repository.

What it shows:
- Public portfolio website
- Modern web presentation for my projects
- A place for a more visual, interactive experience

### 3. [Resturant-app](https://github.com/Mayank7211/Resturant-app)
Full-stack restaurant ordering application.

What it shows:
- End-to-end application design
- JavaScript, Python, CSS, HTML, Docker, and shell scripting
- Real product thinking around ordering and admin workflows

### 4. [ai-reel-automator](https://github.com/Mayank7211/ai-reel-automator)
AI-powered automation tool for reel creation.

What it shows:
- Python-based automation
- Video and engagement processing ideas
- Practical AI/ML-style workflow automation

### 5. [AI Assistant Builder](PROJECTS_INDEX.md)
The main production-style AI system in this workspace.

What it shows:
- FastAPI backend
- Multi-tenant architecture
- LLM integration and routing
- Document ingestion and analytics
- React admin UI and embeddable widget

## What I build

- Python systems with FastAPI and async services
- AI and ML features that can be shipped to real users
- Frontends that are simple to use and strong on presentation
- Tools that are cost-aware, maintainable, and easy to deploy

## Tech stack

- Python
- FastAPI
- React
- Vite
- PostgreSQL
- Docker
- JavaScript
- TypeScript
- TensorFlow interest and ML experimentation

## Why this repo exists

- To give recruiters one clean public place to understand my work
- To make my projects easy to star, browse, and share
- To show both engineering depth and product thinking
- To support a future public site on my own domain

## Public site goals

- Interactive hero section
- Strong visuals and smooth motion
- Project cards with links to GitHub repos
- Clear skills and experience section
- Contact or profile links that are easy to find
- Mobile-friendly and recruiter-friendly layout

## Supporting docs

- [PROJECTS_INDEX.md](PROJECTS_INDEX.md) - project and portfolio index
- [PORTFOLIO_README.md](PORTFOLIO_README.md) - profile summary
- [PROJECT_SHOWCASE.md](PROJECT_SHOWCASE.md) - AI Assistant Builder deep dive
- [SKILLS_AND_EXPERIENCE.md](SKILLS_AND_EXPERIENCE.md) - skills and learning summary
- [RECRUITER_QUICKSTART.md](RECRUITER_QUICKSTART.md) - quick recruiter view
- [GITHUB_UPLOAD_GUIDE.md](GITHUB_UPLOAD_GUIDE.md) - publishing steps

## If you want to run the main project locally

### Docker
1. Run `docker compose up --build`
2. Open the frontend at `http://localhost:3000`
3. Check backend health at `http://localhost:8000/health`

### Backend without Docker
1. Open a terminal in `apps/backend`
2. Create and activate a virtual environment
3. Run `pip install -r requirements.txt`
4. Set `AI_AGENT_DATABASE_URL=sqlite+aiosqlite:///./sql_app.db`
5. Run `uvicorn app.main:app --reload --port 8000`

### Frontend without Docker
1. Open a terminal in `apps/frontend`
2. Run `npm install`
3. Run `npm run dev`
4. Open the local Vite URL

## Current MVP API

- `GET /health`
- `POST /api/tenants`
- `POST /api/tenants/{tenant_id}/knowledge`
- `POST /api/chat`

## Next public-site upgrades

- Deploy the frontend to `mayankaura.me`
- Add a custom animated landing page
- Add live project cards and stars/download links
- Add a contact section and social links
- Add screenshots and visual previews for each project
