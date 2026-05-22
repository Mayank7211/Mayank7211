# Local Testing Guide

## Before You Start

1. **Get Groq API Key** (free):
   - Go to: https://console.groq.com
   - Sign up and get your API key
   - You'll use this in the .env file

2. **Create .env file** in `apps/backend/`:
   ```
   AI_AGENT_ENVIRONMENT=dev
   AI_AGENT_GROQ_API_KEY=your_groq_api_key_here
   AI_AGENT_DATABASE_URL=sqlite+aiosqlite:///./sql_app.db
   AI_AGENT_AUTO_CREATE_TABLES=true
   AI_AGENT_MAX_CONTEXT_CHUNKS=4
   AI_AGENT_REQUEST_TIMEOUT_SECONDS=15
   ```

## Option A: Backend Only (Fastest for Testing)

### If you have Python:

1. **Install dependencies**:
   ```bash
   cd apps/backend
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Start the backend**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   Open: http://localhost:8000

3. **Test the API** (using test_api.py or Postman/curl):
   ```bash
   # From another terminal in apps/backend:
   python test_api.py
   ```

### Test Flow:

1. Create a tenant:
   ```bash
   curl -X POST http://localhost:8000/api/tenants \
     -H "Content-Type: application/json" \
     -d '{
       "business_name": "Maya Skin Clinic",
       "domain": "mayaclinic.com",
       "category": "doctor",
       "description": "Professional skin care clinic",
       "services": ["facials", "consultations"],
       "contact": {"phone": "555-1234", "email": "contact@maya.com"}
     }'
   ```

2. Save the `tenant_id` from response

3. Get a chat response:
   ```bash
   curl -X POST http://localhost:8000/api/chat \
     -H "Content-Type: application/json" \
     -d '{
       "tenant_id": "YOUR_TENANT_ID",
       "message": "Do you offer facial treatments?",
       "session_id": "test-session-123"
     }'
   ```

---

## Option B: Docker (Full Stack)

If you have Docker installed:

```bash
docker compose up --build
```

This starts:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **Database**: postgres on 5432

Then:
1. Open http://localhost:3000
2. Fill the onboarding form
3. Chat with your AI agent
4. Embed code generates automatically

---

## Widget Testing

After creating a business profile, you'll get an embed script. To test locally:

1. Create a test HTML file (test-widget.html):
   ```html
   <!DOCTYPE html>
   <html>
   <body style="padding: 20px;">
     <h1>Test Business Website</h1>
     <p>Your content here...</p>
     
     <!-- Paste your widget embed code below -->
     <script src="http://localhost:8000/widget/agent.js" data-tenant-id="YOUR_TENANT_ID"></script>
   </body>
   </html>
   ```

2. Open the file in a browser
3. Chat button should appear bottom-right

---

## What Gets Tested

✅ **Onboarding** → Create business profile  
✅ **Knowledge Ingestion** → Store business info  
✅ **Chat API** → Send message, get AI response  
✅ **Groq Integration** → Real LLM responses  
✅ **Conversation History** → AI remembers context  
✅ **Reservation Detection** → AI identifies booking intent  
✅ **Widget** → Embeddable chat interface  

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `GROQ_API_KEY not found` | Add to .env file in apps/backend |
| `Module not found` | Run `pip install -r requirements.txt` |
| `Connection refused on 8000` | Backend not running, check `uvicorn app.main:app --reload` |
| `npm install fails` | Skip frontend, test backend + widget separately |
| `CORS error` | Backend CORS middleware already allows `*`, check frontend URL |

---

## Next Steps

1. Test basic flow locally
2. Upload real business documents as knowledge
3. Customize widget colors/position
4. Deploy backend (Heroku, AWS, etc.)
5. Host widget on CDN
6. Integrate with customer's domain
