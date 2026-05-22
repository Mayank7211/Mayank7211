from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import analytics, chat, health, tenants
from app.core.config import settings
from app.core.rate_limits import RateLimitExceeded
from app.db.session import close_db, init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    try:
        yield
    finally:
        await close_db()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", settings.owner_auth_header],
)

app.include_router(health.router)
app.include_router(tenants.router, prefix=settings.api_prefix)
app.include_router(chat.router, prefix=settings.api_prefix)
app.include_router(analytics.router, prefix=settings.api_prefix)


@app.exception_handler(RateLimitExceeded)
async def handle_rate_limit(_: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "detail": exc.detail,
            "retry_after_seconds": exc.retry_after_seconds,
        },
    )

@app.get("/")
def read_root() -> dict:
    return {"message": "AI Agent Builder API is running."}
