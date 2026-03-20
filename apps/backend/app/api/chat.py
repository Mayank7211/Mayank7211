from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rate_limits import RateLimitExceeded, rate_limiter
from app.db.session import get_db_session
from app.models.schemas import ChatRequest, ChatResponse
from app.services.assistant_service import assistant_service

router = APIRouter(prefix="/chat", tags=["chat"])


def _client_ip(request: Request) -> str:
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


async def enforce_chat_rate_limit(request: Request, payload: ChatRequest) -> None:
    key = f"chat:{_client_ip(request)}:{payload.tenant_id}"
    retry_after = rate_limiter.check(key=key, max_requests=20, window_seconds=60)
    if retry_after is not None:
        raise RateLimitExceeded(retry_after_seconds=retry_after, detail="Rate limit exceeded")


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    _: None = Depends(enforce_chat_rate_limit),
    db: AsyncSession = Depends(get_db_session),
) -> ChatResponse:
    return await assistant_service.chat(payload, db)
