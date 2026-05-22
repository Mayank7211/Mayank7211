"""Cross-encoder reranker prototype with a lightweight fallback.

If `sentence_transformers.CrossEncoder` is available it will be used to score
query-passage pairs; otherwise the repo's TF-IDF reranker is used as a
deterministic fallback suitable for CI and smoke tests.
"""
from typing import List, Tuple

try:
    from sentence_transformers import CrossEncoder  # type: ignore
    _HAS_CE = True
except Exception:
    _HAS_CE = False

from . import reranker as tfidf_reranker


class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._model = None
        if _HAS_CE:
            try:
                self._model = CrossEncoder(model_name)
            except Exception:
                self._model = None

    def available(self) -> bool:
        return self._model is not None

    def rerank(self, query: str, passages: List[str]) -> List[Tuple[str, float]]:
        """Return list of (passage, score) sorted desc.

        Falls back to TF-IDF reranker when CrossEncoder isn't available.
        """
        if not passages:
            return []

        if self.available():
            pairs = [(query, p) for p in passages]
            try:
                scores = self._model.predict(pairs)
            except Exception:
                scores = None
            if scores is not None:
                paired = list(zip(passages, [float(s) for s in scores]))
                paired.sort(key=lambda x: x[1], reverse=True)
                return paired

        # Fallback
        tfidf = tfidf_reranker.rerank_tfidf(query, passages)
        # tfidf returns (score, passage)
        return [(p, float(s)) for s, p in tfidf]


def default_reranker() -> CrossEncoderReranker:
    return CrossEncoderReranker()
