from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.entities import ConversationEntity, KnowledgeSourceEntity, TenantEntity, ReservationEntity
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    KnowledgeIngestRequest,
    TenantCreateRequest,
    TenantCreateResponse,
)
from app.services.knowledge import rank_context_blocks
from app.services.model_gateway import (
    BackupOpenModelProvider,
    GroqProvider,
    ModelGateway,
    ModelRequest,
)


class AssistantService:
    def __init__(self, gateway: ModelGateway, max_context_chunks: int) -> None:
        self.gateway = gateway
        self.max_context_chunks = max_context_chunks

    async def create_tenant(self, payload: TenantCreateRequest, db: AsyncSession) -> TenantCreateResponse:
        existing = await db.execute(
            select(TenantEntity.id).where(TenantEntity.domain == payload.domain),
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A tenant with this domain already exists",
            )

        tenant = TenantEntity(
            business_name=payload.business_name,
            domain=payload.domain,
            category=payload.category,
            description=payload.description,
            contact_phone=payload.contact.phone,
            contact_email=payload.contact.email,
            contact_whatsapp=payload.contact.whatsapp,
        )
        db.add(tenant)
        await db.flush()

        seed_knowledge = [
            payload.description,
            *(f"Service: {service}" for service in payload.services),
            *(f"FAQ: {faq.question} -> {faq.answer}" for faq in payload.faqs),
        ]
        for block in [item.strip() for item in seed_knowledge if item and item.strip()]:
            db.add(
                KnowledgeSourceEntity(
                    tenant_id=tenant.id,
                    source_type="seed",
                    source_label="onboarding",
                    raw_text=block,
                    source_metadata={},
                ),
            )

        await db.commit()

        widget_embed_script = (
            "<script src='https://cdn.your-app.com/widget.js' "
            f"data-tenant-id='{tenant.id}' "
            "data-theme='light' "
            "data-position='bottom-right' "
            "data-primary-color='#0f766e'></script>"
        )
        return TenantCreateResponse(
            tenant_id=str(tenant.id),
            widget_embed_script=widget_embed_script,
        )

    async def ingest_knowledge(self, tenant_id: str, payload: KnowledgeIngestRequest, db: AsyncSession) -> dict:
        tenant = await db.get(TenantEntity, tenant_id)
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found",
            )

        clean_blocks = [item.strip() for item in payload.text_blocks if item and item.strip()]
        for block in clean_blocks:
            db.add(
                KnowledgeSourceEntity(
                    tenant_id=tenant_id,
                    source_type="manual",
                    source_label=str(payload.source_url) if payload.source_url else "manual",
                    raw_text=block,
                    source_metadata={},
                ),
            )

        await db.commit()

        return {
            "tenant_id": tenant_id,
            "indexed_blocks": len(clean_blocks),
            "source_url": str(payload.source_url) if payload.source_url else None,
        }

    async def _load_context(self, tenant_id: str, query: str, db: AsyncSession) -> list[str]:
        result = await db.execute(
            select(KnowledgeSourceEntity.raw_text)
            .where(KnowledgeSourceEntity.tenant_id == tenant_id)
            .order_by(KnowledgeSourceEntity.created_at.desc())
            .limit(400),
        )
        blocks = [item for item in result.scalars().all() if item]
        return rank_context_blocks(blocks, query, self.max_context_chunks)

    async def _load_conversation_history(self, tenant_id: str, session_id: str | None, db: AsyncSession) -> list[dict]:
        """Load recent conversation history for context continuity."""
        if not session_id:
            return []
        
        result = await db.execute(
            select(ConversationEntity.user_message, ConversationEntity.assistant_message)
            .where(
                ConversationEntity.tenant_id == tenant_id,
                ConversationEntity.session_id == session_id,
            )
            .order_by(ConversationEntity.created_at.asc())
            .limit(10),  # Last 10 exchanges
        )
        
        history = []
        for user_msg, assistant_msg in result.all():
            history.append({"role": "user", "content": user_msg})
            history.append({"role": "assistant", "content": assistant_msg})
        
        return history

    def _detect_reservation_intent(self, message: str, response: str) -> bool:
        """Check if user is trying to book an appointment/reservation."""
        reservation_keywords = [
            "book", "appointment", "reservation", "schedule", "meeting",
            "time", "date", "slot", "available", "when", "what time",
            "can i", "would like to", "want to", "need to"
        ]
        
        combined_text = (message + " " + response).lower()
        return sum(1 for keyword in reservation_keywords if keyword in combined_text) >= 2

    async def chat(self, payload: ChatRequest, db: AsyncSession) -> ChatResponse:
        tenant = await db.get(TenantEntity, payload.tenant_id)
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found",
            )

        context = await self._load_context(payload.tenant_id, payload.message, db)
        conversation_history = await self._load_conversation_history(payload.tenant_id, payload.session_id, db)

        model_request = ModelRequest(
            tenant_id=payload.tenant_id,
            business_name=tenant.business_name,
            category=tenant.category,
            message=payload.message,
            context_chunks=context,
            conversation_history=conversation_history,
        )
        model_response = await self.gateway.complete(model_request)

        handoff_recommended = model_response.confidence < 0.5
        reservation_detected = self._detect_reservation_intent(payload.message, model_response.answer)
        
        db.add(
            ConversationEntity(
                tenant_id=payload.tenant_id,
                session_id=payload.session_id,
                user_message=payload.message,
                assistant_message=model_response.answer,
                provider=model_response.provider,
                model=model_response.model,
                confidence=model_response.confidence,
                handoff_recommended=handoff_recommended,
            ),
        )
        await db.commit()

        return ChatResponse(
            answer=model_response.answer,
            provider=model_response.provider,
            model=model_response.model,
            confidence=model_response.confidence,
            handoff_recommended=handoff_recommended,
            reservation_detected=reservation_detected,
        )


assistant_service = AssistantService(
    gateway=ModelGateway(
        providers=[GroqProvider(api_key=settings.groq_api_key), BackupOpenModelProvider()],
    ),
    max_context_chunks=settings.max_context_chunks,
)
