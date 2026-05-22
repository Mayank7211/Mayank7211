from collections import Counter
import math
from typing import List, Tuple


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in __import__('re').findall(r"[a-zA-Z0-9]+", text)]


def build_tfidf(docs: List[str]) -> Tuple[List[Counter], dict]:
    """Build TF and IDF structures for a list of documents.

    Returns (tf_counters, idf_dict)
    """
    tf_counters = []
    df = Counter()
    for d in docs:
        toks = _tokenize(d)
        c = Counter(toks)
        tf_counters.append(c)
        for t in set(toks):
            df[t] += 1

    idf = {}
    n = len(docs)
    for term, dfreq in df.items():
        idf[term] = math.log((n + 1) / (dfreq + 1)) + 1.0

    return tf_counters, idf


def score_tfidf(query: str, docs: List[str], tf_counters=None, idf=None) -> List[float]:
    """Score docs by TF-IDF similarity to query. Returns list of scores in same order as docs."""
    q_tokens = _tokenize(query)
    qtf = Counter(q_tokens)

    if tf_counters is None or idf is None:
        tf_counters, idf = build_tfidf(docs)

    scores = []
    for tf in tf_counters:
        s = 0.0
        for term, qcount in qtf.items():
            if term in idf:
                s += (qcount * idf.get(term, 0.0) * tf.get(term, 0))
        scores.append(s)

    # Normalize by document length to reduce bias toward longer docs
    norm_scores = []
    for sc, d in zip(scores, docs):
        l = max(1, len(_tokenize(d)))
        norm_scores.append(sc / l)

    return norm_scores


def rerank(query: str, candidates: List[str]) -> List[Tuple[str, float]]:
    """Return candidates re-ranked by TF-IDF score (highest first).

    Each item is (doc, score).
    """
    if not candidates:
        return []
    tf_counters, idf = build_tfidf(candidates)
    scores = score_tfidf(query, candidates, tf_counters, idf)
    paired = list(zip(candidates, scores))
    paired.sort(key=lambda x: x[1], reverse=True)
    return paired
"""Simple reranker prototypes.

Provides a minimal TF-IDF-like rescoring function implemented without
external dependencies so it can run in CI and test environments.
"""
from collections import Counter
import math
from typing import List, Tuple


def _tokenize(text: str) -> List[str]:
    return [t for t in text.lower().split() if t]


def rerank_tfidf(query: str, passages: List[str]) -> List[Tuple[float, str]]:
    """Return passages scored by a simple TF-IDF style weighting.

    Returns a list of (score, passage) sorted by descending score.
    """
    docs_tokens = [_tokenize(p) for p in passages]
    N = len(docs_tokens)

    # document frequency
    df = Counter()
    for toks in docs_tokens:
        df.update(set(toks))

    idf = {}
    for term, cnt in df.items():
        idf[term] = math.log((N + 1) / (cnt + 1)) + 1.0

    q_tokens = _tokenize(query)
    scores = []
    for p, toks in zip(passages, docs_tokens):
        tf = Counter(toks)
        score = 0.0
        for t in q_tokens:
            score += tf.get(t, 0) * idf.get(t, 0.0)
        scores.append((score, p))

    scores.sort(key=lambda x: x[0], reverse=True)
    return scores
