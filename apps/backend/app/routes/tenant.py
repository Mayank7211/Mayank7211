from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.tenant import Tenant, Agent
from ..schemas import TenantCreate, TenantResponse, AgentCreate, AgentResponse

router = APIRouter()

@router.post("/tenants/", response_model=TenantResponse)
def create_tenant(tenant: TenantCreate, db: Session = Depends(get_db)):
    db_tenant = Tenant(**tenant.model_dump())
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant

@router.get("/tenants/{tenant_id}", response_model=TenantResponse)
def read_tenant(tenant_id: int, db: Session = Depends(get_db)):
    db_tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant

@router.post("/tenants/{tenant_id}/agents/", response_model=AgentResponse)
def create_agent_for_tenant(tenant_id: int, agent: AgentCreate, db: Session = Depends(get_db)):
    db_tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not db_tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
        
    db_agent = Agent(**agent.model_dump(), tenant_id=tenant_id, system_prompt="Answer politely and helpfully.")
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent
