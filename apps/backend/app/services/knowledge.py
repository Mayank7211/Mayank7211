import re
from typing import Iterable, List

def rank_context_blocks(blocks: Iterable[str], query: str, limit: int) -> List[str]:
    knowledge = [item for item in blocks if item and item.strip()]
    if not knowledge or limit <= 0:
        return []

    tokens = set(re.findall(r"[a-zA-Z0-9]+", query.lower()))
    scored = []

    for block in knowledge:
        block_tokens = set(re.findall(r"[a-zA-Z0-9]+", block.lower()))
        overlap = len(tokens.intersection(block_tokens))
        scored.append((overlap, block))

    scored.sort(key=lambda item: item[0], reverse=True)
    top = [item[1] for item in scored[:limit]]
    return top
