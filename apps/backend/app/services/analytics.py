from datetime import datetime, timedelta
from typing import List, Dict, Any

from sqlalchemy import func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import ConversationEntity, TenantEntity, ReservationEntity, KnowledgeSourceEntity


class AnalyticsService:
    """Service for tracking and analyzing usage metrics."""
    
    async def get_tenant_stats(self, tenant_id: str, db: AsyncSession) -> Dict[str, Any]:
        """Get statistics for a specific tenant."""
        
        # Total conversations
        conv_result = await db.execute(
            select(func.count(ConversationEntity.id)).where(
                ConversationEntity.tenant_id == tenant_id
            )
        )
        total_conversations = conv_result.scalar() or 0
        
        # Total reservations
        res_result = await db.execute(
            select(func.count(ReservationEntity.id)).where(
                ReservationEntity.tenant_id == tenant_id
            )
        )
        total_reservations = res_result.scalar() or 0
        
        # Pending reservations
        pending_result = await db.execute(
            select(func.count(ReservationEntity.id)).where(
                and_(
                    ReservationEntity.tenant_id == tenant_id,
                    ReservationEntity.status == "pending"
                )
            )
        )
        pending_reservations = pending_result.scalar() or 0
        
        # Total knowledge chunks
        knowledge_result = await db.execute(
            select(func.count(KnowledgeSourceEntity.id)).where(
                KnowledgeSourceEntity.tenant_id == tenant_id
            )
        )
        total_knowledge = knowledge_result.scalar() or 0
        
        # Handoff rate
        handoff_result = await db.execute(
            select(func.count(ConversationEntity.id)).where(
                and_(
                    ConversationEntity.tenant_id == tenant_id,
                    ConversationEntity.handoff_recommended == True
                )
            )
        )
        handoff_count = handoff_result.scalar() or 0
        handoff_rate = (handoff_count / total_conversations * 100) if total_conversations > 0 else 0
        
        # Conversations last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        week_result = await db.execute(
            select(func.count(ConversationEntity.id)).where(
                and_(
                    ConversationEntity.tenant_id == tenant_id,
                    ConversationEntity.created_at >= seven_days_ago
                )
            )
        )
        conversations_this_week = week_result.scalar() or 0
        
        return {
            "total_conversations": total_conversations,
            "total_reservations": total_reservations,
            "pending_reservations": pending_reservations,
            "total_knowledge_chunks": total_knowledge,
            "handoff_rate": round(handoff_rate, 2),
            "conversations_this_week": conversations_this_week,
        }
    
    async def get_recent_conversations(
        self, tenant_id: str, limit: int = 20, db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """Get recent conversations for a tenant."""
        result = await db.execute(
            select(
                ConversationEntity.id,
                ConversationEntity.user_message,
                ConversationEntity.assistant_message,
                ConversationEntity.created_at,
                ConversationEntity.handoff_recommended,
                ConversationEntity.confidence
            )
            .where(ConversationEntity.tenant_id == tenant_id)
            .order_by(ConversationEntity.created_at.desc())
            .limit(limit)
        )
        
        conversations = []
        for row in result:
            conversations.append({
                "id": row[0],
                "user_message": row[1],
                "assistant_message": row[2],
                "timestamp": row[3].isoformat() if row[3] else None,
                "handoff_required": row[4],
                "confidence": round(row[5], 2) if row[5] else 0,
            })
        
        return conversations
    
    async def get_pending_reservations(
        self, tenant_id: str, limit: int = 50, db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """Get pending reservations for a tenant."""
        result = await db.execute(
            select(
                ReservationEntity.id,
                ReservationEntity.customer_name,
                ReservationEntity.customer_phone,
                ReservationEntity.customer_email,
                ReservationEntity.service_requested,
                ReservationEntity.preferred_date,
                ReservationEntity.preferred_time,
                ReservationEntity.created_at,
                ReservationEntity.status
            )
            .where(
                and_(
                    ReservationEntity.tenant_id == tenant_id,
                    ReservationEntity.status == "pending"
                )
            )
            .order_by(ReservationEntity.created_at.desc())
            .limit(limit)
        )
        
        reservations = []
        for row in result:
            reservations.append({
                "id": row[0],
                "customer_name": row[1],
                "customer_phone": row[2],
                "customer_email": row[3],
                "service": row[4],
                "preferred_date": row[5],
                "preferred_time": row[6],
                "created_at": row[7].isoformat() if row[7] else None,
                "status": row[8],
            })
        
        return reservations
    
    async def get_daily_metrics(
        self, tenant_id: str, days: int = 30, db: AsyncSession = None
    ) -> List[Dict[str, Any]]:
        """Get daily conversation metrics for the last N days."""
        metrics = []
        
        for i in range(days):
            date = datetime.utcnow().date() - timedelta(days=i)
            start = datetime.combine(date, datetime.min.time())
            end = datetime.combine(date, datetime.max.time())
            
            count_result = await db.execute(
                select(func.count(ConversationEntity.id)).where(
                    and_(
                        ConversationEntity.tenant_id == tenant_id,
                        ConversationEntity.created_at >= start,
                        ConversationEntity.created_at <= end
                    )
                )
            )
            count = count_result.scalar() or 0
            
            metrics.append({
                "date": date.isoformat(),
                "conversations": count,
            })
        
        # Reverse to show oldest first
        return list(reversed(metrics))
    
    async def get_confidence_distribution(
        self, tenant_id: str, db: AsyncSession = None
    ) -> Dict[str, int]:
        """Get distribution of AI response confidence levels."""
        result = await db.execute(
            select(ConversationEntity.confidence).where(
                ConversationEntity.tenant_id == tenant_id
            )
        )
        
        confidences = [row[0] for row in result if row[0] is not None]
        
        if not confidences:
            return {"high": 0, "medium": 0, "low": 0}
        
        high = sum(1 for c in confidences if c >= 0.7)
        medium = sum(1 for c in confidences if 0.4 <= c < 0.7)
        low = sum(1 for c in confidences if c < 0.4)
        
        return {
            "high": high,
            "medium": medium,
            "low": low,
        }


analytics_service = AnalyticsService()
