from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_owner_tenant_access
from app.db.session import get_db_session
from app.models.entities import TenantEntity
from app.services.analytics import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/tenants/{tenant_id}/stats")
async def get_tenant_stats(
    tenant_id: str,
    _owner_access: None = Depends(require_owner_tenant_access),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    """Get usage statistics for a tenant."""
    # Verify tenant exists
    tenant = await db.get(TenantEntity, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    
    stats = await analytics_service.get_tenant_stats(tenant_id, db)
    return stats


@router.get("/tenants/{tenant_id}/conversations")
async def get_tenant_conversations(
    tenant_id: str,
    limit: int = 20,
    _owner_access: None = Depends(require_owner_tenant_access),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    """Get recent conversations for a tenant."""
    tenant = await db.get(TenantEntity, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    
    conversations = await analytics_service.get_recent_conversations(
        tenant_id, limit=limit, db=db
    )
    return {
        "tenant_id": tenant_id,
        "count": len(conversations),
        "conversations": conversations,
    }


@router.get("/tenants/{tenant_id}/reservations")
async def get_pending_reservations(
    tenant_id: str,
    _owner_access: None = Depends(require_owner_tenant_access),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    """Get pending reservations for a tenant."""
    tenant = await db.get(TenantEntity, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    
    reservations = await analytics_service.get_pending_reservations(
        tenant_id, db=db
    )
    return {
        "tenant_id": tenant_id,
        "count": len(reservations),
        "reservations": reservations,
    }


@router.get("/tenants/{tenant_id}/daily-metrics")
async def get_daily_metrics(
    tenant_id: str,
    days: int = 30,
    _owner_access: None = Depends(require_owner_tenant_access),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    """Get daily conversation metrics."""
    tenant = await db.get(TenantEntity, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    
    # Limit days to reasonable range
    days = min(max(days, 7), 90)
    
    metrics = await analytics_service.get_daily_metrics(tenant_id, days=days, db=db)
    return {
        "tenant_id": tenant_id,
        "days": days,
        "metrics": metrics,
    }


@router.get("/tenants/{tenant_id}/confidence")
async def get_confidence_distribution(
    tenant_id: str,
    _owner_access: None = Depends(require_owner_tenant_access),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    """Get distribution of AI confidence levels."""
    tenant = await db.get(TenantEntity, tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found",
        )
    
    dist = await analytics_service.get_confidence_distribution(tenant_id, db=db)
    return {
        "tenant_id": tenant_id,
        "confidence_distribution": dist,
    }
