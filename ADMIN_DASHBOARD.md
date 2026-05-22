# Admin Dashboard Guide

## Overview

The Admin Dashboard gives you real-time insights into your AI assistant's performance and customer interactions.

## Features

### 1. Overview Tab
High-level metrics about your AI assistant:
- **Total Conversations** - All chats since creation
- **This Week** - Conversations in the last 7 days
- **Handoff Rate** - % of conversations escalated to humans (indicates low confidence)
- **Total Reservations** - All booking requests received
- **Pending** - Reservations awaiting confirmation
- **Knowledge Chunks** - Uploaded documents and text blocks

### 2. Conversations Tab
View recent customer interactions:
- **Latest 10 conversations** shown first
- Each shows:
  - **Customer Message** - What the user asked
  - **AI Response** - What the assistant answered
  - **Timestamp** - When it happened
  - **Confidence** - How sure the AI was (0-100%)
  - **Escalation Label** - If conversation was marked for human review

**What to look for:**
- Low confidence scores (<40%) = conversation quality issues
- Escalated conversations = complex questions the AI couldn't handle
- Common patterns = knowledge gaps to fill

### 3. Reservations Tab
Track appointment/booking requests:
- Shows all **pending reservations** waiting for confirmation
- Columns:
  - **Name** - Customer name (extracted by AI)
  - **Service** - What the customer wants to book
  - **Date & Time** - Preferred appointment
  - **Contact** - Phone and email for follow-up
  - **Status** - Current status (pending/confirmed/completed)

**Action items:**
- Contact pending customers within 24 hours
- Confirm or reschedule as needed
- Update status in database

---

## API Endpoints

All endpoints require a `tenant_id` (your business ID).

### Get Stats
```
GET /api/analytics/tenants/{tenant_id}/stats
```
Returns: Total conversations, reservations, pending, handoff rate, weekly stats

### Get Recent Conversations  
```
GET /api/analytics/tenants/{tenant_id}/conversations?limit=20
```
Returns: List of recent conversations with messages, timestamps, confidence

### Get Pending Reservations
```
GET /api/analytics/tenants/{tenant_id}/reservations
```
Returns: List of pending reservations with customer info and preferences

### Get Daily Metrics
```
GET /api/analytics/tenants/{tenant_id}/daily-metrics?days=30
```
Returns: Conversation count per day for last 30 days (good for trends)

### Get Confidence Distribution
```
GET /api/analytics/tenants/{tenant_id}/confidence
```
Returns: How many conversations had high/medium/low confidence

---

## Using the Dashboard

### Access from Frontend
In your React app:
```tsx
import AdminDashboard from "./components/AdminDashboard";

export default function Analytics() {
  const tenantId = "your-tenant-id"; // From onboarding
  return <AdminDashboard tenantId={tenantId} />;
}
```

### Standalone Access
Use the API directly from any tool (dashboard, terminal, spreadsheet):
```bash
curl http://localhost:8000/api/analytics/tenants/YOUR_TENANT_ID/stats
```

### Refresh Rate
Dashboard auto-refreshes every 30 seconds. Click "Refresh" button for immediate update.

---

## Key Metrics Explained

### Handoff Rate (Should be < 20%)
- **High rate (>40%)**: Too many escalations
  - *Fix:* Upload more knowledge documents
  - *Fix:* Add FAQs that customers ask about
  - *Fix:* Verify AI system prompt is correct

- **Low rate (<5%)**: Good! AI is handling most questions
  - *Monitor:* Spot-check some low-confidence conversations

### Confidence Score
- **High (80-100%)**: AI is very sure of the answer
- **Medium (40-80%)**: Answer is reasonable but not certain
- **Low (0-40%)**: AI is guessing; escalate to human

### Conversation Trends (Daily Metrics)
- **Increasing over weeks?** Business is getting more visibility
- **Flat or decreasing?** May need to promote the chat widget
- **Spikes on certain days?** Find patterns (weekends? after emails?)

### Reservation Metrics
- **High pending count?** Need faster follow-up process
- **Low conversion?** May need to improve booking confirmation message

---

## Best Practices

### Daily
- Check pending reservations (respond within 24 hours)
- Review any conversations marked for escalation

### Weekly
- Look at handoff rate trend
- Identify top missing knowledge areas
- Update knowledge base based on questions

### Monthly
- Analyze conversation trends
- Check customer satisfaction
- Plan new features or improvements

---

## Troubleshooting

**Dashboard shows 0 conversations?**
- Widget may not be embedded yet
- Check that customers are actually chatting
- Verify tenant ID is correct

**High handoff rate (>50%)?**
- Upload your business documents/manuals to knowledge base
- Add FAQs based on real customer questions
- Improve system prompt in model gateway

**Confidence scores all low?**
- Not enough knowledge base context
- AI model might not match question complexity
- Try Groq model instead of local

---

## Integrations

### Export to Spreadsheet
Copy stats to Google Sheets or Excel:
```bash
# Get all stats as JSON
curl http://localhost:8000/api/analytics/tenants/TENANT_ID/stats | \
  jq . # Format as JSON
```

### Webhook Integration (Future)
POST conversation events to your system when:
- Reservation is created
- Handoff is triggered
- Daily summary generated

### Slack Notifications (Future)
Auto-send pending reservation count to Slack daily

---

## Performance Optimization

The dashboard loads fast because:
- Stats are pre-calculated at query time
- Limited to last 30 days of data
- Conversations paginate (20 at a time)

For large volumes (1000s of conversations):
- Limit daily-metrics days parameter
- Archive old conversations monthly
- Add caching layer

---

**Questions?** Check the main README or contact support.
