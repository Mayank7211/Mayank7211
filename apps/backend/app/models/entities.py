from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, JSON, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class TenantEntity(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    business_name: Mapped[str] = mapped_column(String(120), nullable=False)
    domain: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    contact_phone: Mapped[str | None] = mapped_column(String(60), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_whatsapp: Mapped[str | None] = mapped_column(String(60), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class KnowledgeSourceEntity(Base):
    __tablename__ = "knowledge_sources"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    tenant_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), ForeignKey("tenants.id", ondelete="CASCADE"), index=True)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    source_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_metadata: Mapped[dict] = mapped_column("metadata", JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class ConversationEntity(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    tenant_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), ForeignKey("tenants.id", ondelete="CASCADE"), index=True)
    session_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_message: Mapped[str] = mapped_column(Text, nullable=False)
    assistant_message: Mapped[str] = mapped_column(Text, nullable=False)
    provider: Mapped[str | None] = mapped_column(String(120), nullable=True)
    model: Mapped[str | None] = mapped_column(String(120), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    handoff_recommended: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class ReservationEntity(Base):
    __tablename__ = "reservations"

    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    tenant_id: Mapped[str] = mapped_column(Uuid(as_uuid=False), ForeignKey("tenants.id", ondelete="CASCADE"), index=True)
    session_id: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    customer_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    customer_phone: Mapped[str | None] = mapped_column(String(60), nullable=True)
    customer_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    service_requested: Mapped[str | None] = mapped_column(String(255), nullable=True)
    preferred_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    preferred_time: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")  # pending, confirmed, completed, cancelled
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
