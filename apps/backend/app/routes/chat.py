from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.tenant import Tenant, Agent
from ..schemas import ChatRequest, ChatResponse
import os
import groq

router = APIRouter()

# Initialize Groq client
# We'll use the API key from the environment/settings
groq_client = groq.Groq(api_key=os.environ.get("AI_AGENT_GROQ_API_KEY", ""))

@router.post("/chat/{agent_id}", response_model=ChatResponse)
async def chat_with_agent(agent_id: int, request: ChatRequest, db: Session = Depends(get_db)):
    # 1. Fetch the Agent to get their system prompt
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    tenant = agent.tenant
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant associated with Agent not found")

    # 2. Build the System Prompt
    # In a real MVP we would probably assemble this from Tenant.faqs, Tenant.services etc.
    # For now we use the basic agent system_prompt + tenant tone.
    system_message_content = f"""You are a helpful AI assistant for a business named '{tenant.name}'.
You must adopt a '{tenant.tone_of_voice}' tone of voice.

Business Context / Services:
{tenant.business_services or "Not provided"}

Frequently Asked Questions:
{tenant.faqs or "Not provided"}

Additional Rules:
- {agent.system_prompt or "Be concise and helpful."}
- Do not make up prices or services not listed in the context. If you don't know, ask the user to call the business.
"""

    messages = [{"role": "system", "content": system_message_content}]
    
    # 3. Add History
    for msg in request.history:
        messages.append({"role": msg.role, "content": msg.content})
        
    # 4. Add the latest user message
    messages.append({"role": "user", "content": request.message})

    # 5. Call LLM (Groq Llama-3)
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192", # Super fast and very cheap open model
            max_tokens=512,
            temperature=0.7,
        )
        response_text = chat_completion.choices[0].message.content
        return ChatResponse(response=response_text)
    except Exception as e:
        # Fallback or error handling
        print(f"Error calling LLM: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response from AI")
