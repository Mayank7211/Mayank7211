from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_owner_tenant_access
from app.db.session import get_db_session
from app.models.schemas import KnowledgeIngestRequest, TenantCreateRequest, TenantCreateResponse
from app.services.assistant_service import assistant_service
from app.services.document_parser import parse_document

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("", response_model=TenantCreateResponse)
async def create_tenant(
    payload: TenantCreateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> TenantCreateResponse:
    return await assistant_service.create_tenant(payload, db)


@router.post("/{tenant_id}/knowledge")
async def ingest_knowledge(
    tenant_id: str,
    payload: KnowledgeIngestRequest,
    _owner_access: None = Depends(require_owner_tenant_access),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    return await assistant_service.ingest_knowledge(tenant_id, payload, db)


@router.post("/{tenant_id}/upload")
async def upload_document(
    tenant_id: str,
    file: UploadFile = File(...),
    _owner_access: None = Depends(require_owner_tenant_access),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    """Upload and parse a document (PDF, DOCX, TXT) to knowledge base."""
    # Validate file type
    allowed_types = ['.pdf', '.docx', '.txt']
    file_ext = '.' + (file.filename.split('.')[-1]).lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed: {', '.join(allowed_types)}"
        )
    
    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()
    
    if len(file_content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size: 10MB"
        )
    
    try:
        # Parse document
        chunks = await parse_document(file.filename, file_content)
        
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document is empty or couldn't be parsed"
            )
        
        # Ingest chunks as knowledge
        payload = KnowledgeIngestRequest(
            text_blocks=chunks,
            source_url=None
        )
        result = await assistant_service.ingest_knowledge(tenant_id, payload, db)
        
        return {
            "tenant_id": tenant_id,
            "filename": file.filename,
            "chunks_processed": len(chunks),
            "total_characters": sum(len(c) for c in chunks),
            "message": f"Successfully uploaded and processed {file.filename}"
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )
