from collections import defaultdict
from typing import Dict, List

from app.models.schemas import TenantProfile


TENANT_STORE: Dict[str, TenantProfile] = {}
KNOWLEDGE_STORE: Dict[str, List[str]] = defaultdict(list)
