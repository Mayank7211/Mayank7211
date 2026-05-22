import re
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, HttpUrl, field_validator


_DOMAIN_PATTERN = re.compile(
    r"^(?=.{3,255}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$",
)


class FAQItem(BaseModel):
    question: str = Field(min_length=3, max_length=300)
    answer: str = Field(min_length=1, max_length=1200)


class ContactInfo(BaseModel):
    phone: Optional[str] = None
    email: Optional[str] = None
    whatsapp: Optional[str] = None


class TenantCreateRequest(BaseModel):
    business_name: str = Field(max_length=120)
    domain: str = Field(max_length=255)
    category: str = Field(max_length=80)
    services: List[str] = Field(min_length=1, max_length=50)
    description: str = Field(default="", max_length=2000)
    faqs: List[FAQItem] = Field(default_factory=list, max_length=100)
    contact: ContactInfo = Field(default_factory=ContactInfo)

    @field_validator("business_name", "category")
    @classmethod
    def validate_required_text_fields(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 2:
            raise ValueError("must not be blank")
        return cleaned

    @field_validator("domain")
    @classmethod
    def validate_domain(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if not cleaned or any(separator in cleaned for separator in (" ", "/", "?", "#", "://")):
            raise ValueError("must be a valid domain name like example.com")
        if not _DOMAIN_PATTERN.fullmatch(cleaned):
            raise ValueError("must be a valid domain name like example.com")
        return cleaned

    @field_validator("services")
    @classmethod
    def validate_services(cls, value: List[str]) -> List[str]:
        cleaned: List[str] = []
        for item in value:
            normalized = item.strip()
            if not normalized:
                raise ValueError("services entries must be non-empty strings")
            cleaned.append(normalized)
        return cleaned


class TenantProfile(BaseModel):
    tenant_id: str = Field(default_factory=lambda: str(uuid4()))
    business_name: str
    domain: str
    category: str
    services: List[str] = Field(default_factory=list)
    description: str = ""
    faqs: List[FAQItem] = Field(default_factory=list)
    contact: ContactInfo = Field(default_factory=ContactInfo)


class TenantCreateResponse(BaseModel):
    tenant_id: str
    widget_embed_script: str


class KnowledgeIngestRequest(BaseModel):
    text_blocks: List[str] = Field(default_factory=list, max_length=200)
    source_url: Optional[HttpUrl] = None


class ChatRequest(BaseModel):
    tenant_id: str
    message: str = Field(min_length=1, max_length=3000)
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    provider: str
    model: str
    confidence: float
    handoff_recommended: bool
    reservation_detected: bool = False
    fallback_reason: Optional[str] = None
