from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    domain_name = Column(String, unique=True, index=True)
    
    # Store settings/context for that business
    business_services = Column(Text, nullable=True)
    faqs = Column(Text, nullable=True)
    tone_of_voice = Column(String, default="professional")

    agents = relationship("Agent", back_populates="tenant")

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    name = Column(String)
    system_prompt = Column(Text) # In reality, we could construct this on the fly based on Tenant data
    
    tenant = relationship("Tenant", back_populates="agents")
    # conversations = relationship("Conversation", back_populates="agent")
