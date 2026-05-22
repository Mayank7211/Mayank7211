from dataclasses import dataclass
from typing import List, Protocol

from groq import AsyncGroq

from app.core.config import settings


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


class ModelProvider(Protocol):
    name: str

    async def generate(self, request: ModelRequest, model_name: str) -> ModelResult:
        ...


class GroqProvider:
    name = "groq"

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("GROQ_API_KEY is required")
        self.client = AsyncGroq(api_key=api_key)

    async def generate(self, request: ModelRequest, model_name: str) -> ModelResult:
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

        try:
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
        except Exception as e:
            raise RuntimeError(f"Groq API error: {str(e)}")


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
        except Exception:
            if len(self.providers) == 1:
                raise
            fallback = self.providers[1]
            return await fallback.generate(request, selected_model)
