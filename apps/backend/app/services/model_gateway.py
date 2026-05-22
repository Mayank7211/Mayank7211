import logging
from dataclasses import dataclass
from typing import List, Protocol, Optional

from groq import AsyncGroq, RateLimitError, APIConnectionError, APIError

from app.core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class ModelRequest:
    tenant_id: str
    business_name: str
    category: str
    message: str
    context_chunks: List[str]
    conversation_history: List[dict] = None  # List of {"role": "user/assistant", "content": "..."}


@dataclass
class ModelResult:
    answer: str
    provider: str
    model: str
    confidence: float
    fallback_reason: Optional[str] = None


class ModelProvider(Protocol):
    name: str

    async def generate(self, request: ModelRequest, model_name: str) -> ModelResult:
        ...


class GroqProvider:
    name = "groq"

    def __init__(self, api_key: str) -> None:
        # Avoid raising error if api_key is None for testing purposes
        self.client = AsyncGroq(api_key=api_key) if api_key else None

    async def generate(self, request: ModelRequest, model_name: str) -> ModelResult:
        if not self.client:
            raise RuntimeError("GroqProvider initialized without API key")

        # Build context-aware system prompt
        context_text = " ".join(request.context_chunks).strip()
        if not context_text:
            context_text = "No business context available yet."

        system_prompt = f"""You are a professional AI assistant for {request.business_name}, a {request.category}.

Business Context:
{context_text}

Your responsibilities:
1. Provide accurate information about the business
2. Help with appointment/reservation bookings
3. Answer common questions professionally
4. Suggest relevant services when appropriate
5. Escalate complex issues to humans when needed

When a customer wants to book an appointment or make a reservation:
- Extract their name, phone/email, preferred date & time, and service needed
- Confirm the details back to them
- Never make up information - only confirm what they explicitly state

Keep responses concise, friendly, and professional. Always be helpful and honest.
If you don't know something, admit it and offer to connect them with a person."""

        # Build messages with conversation history
        messages = []
        if request.conversation_history:
            messages.extend(request.conversation_history)
        messages.append({"role": "user", "content": request.message})

        response = await self.client.messages.create(
            model=model_name,
            system=system_prompt,
            messages=messages,
            max_tokens=512,
            temperature=0.7,
        )

        # Extract text from response
        answer = response.choices[0].message.content if response.choices else "No response generated"

        return ModelResult(
            answer=answer,
            provider=self.name,
            model=model_name,
            confidence=0.85,
        )


class BackupOpenModelProvider:
    name = "backup-open-provider"

    async def generate(self, request: ModelRequest, model_name: str) -> ModelResult:
        answer = (
            f"I'm having temporary difficulty connecting to my primary system. "
            f"Please contact {request.business_name} directly via phone or email for immediate assistance. "
            f"Your question was: {request.message}"
        )
        return ModelResult(
            answer=answer,
            provider=self.name,
            model=model_name,
            confidence=0.45,
        )


class ModelGateway:
    def __init__(self, providers: List[ModelProvider]) -> None:
        if not providers:
            raise ValueError("ModelGateway requires at least one provider")
        self.providers = providers

    def _select_model(self, message: str) -> str:
        # Route short prompts to cheaper models and longer prompts to stronger models.
        if len(message) < 220:
            return settings.default_small_model
        return settings.default_large_model

    async def complete(self, request: ModelRequest) -> ModelResult:
        selected_model = self._select_model(request.message)
        primary = self.providers[0]

        try:
            return await primary.generate(request, selected_model)
        except Exception as e:
            fallback_reason = "unknown_error"
            if isinstance(e, RateLimitError):
                fallback_reason = "rate_limit_exceeded"
                logger.warning(f"Groq API rate limit exceeded: {str(e)}")
            elif isinstance(e, APIConnectionError):
                fallback_reason = "api_connection_error"
                logger.error(f"Groq API connection error: {str(e)}")
            elif isinstance(e, APIError):
                fallback_reason = "api_error"
                logger.error(f"Groq API error: {str(e)}")
            else:
                logger.error(f"Groq primary provider failed unexpectedly: {str(e)}")

            if len(self.providers) == 1:
                raise
            
            fallback = self.providers[1]
            result = await fallback.generate(request, selected_model)
            result.fallback_reason = fallback_reason
            return result
