from pydantic import BaseModel
from typing import Optional, List

# ---- Tenant Schemas ----
class TenantBase(BaseModel):
    name: str
    domain_name: str
    business_services: Optional[str] = None
    faqs: Optional[str] = None
    tone_of_voice: Optional[str] = "professional"

class TenantCreate(TenantBase):
    pass

class TenantResponse(TenantBase):
    id: int

    class Config:
        from_attributes = True

# ---- Agent Schemas ----
class AgentBase(BaseModel):
    name: str

class AgentCreate(AgentBase):
    pass

class AgentResponse(AgentBase):
    id: int
    tenant_id: int
    system_prompt: str

    class Config:
        from_attributes = True

# ---- Chat Schemas ----
class ChatMessage(BaseModel):
    role: str # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    response: str
