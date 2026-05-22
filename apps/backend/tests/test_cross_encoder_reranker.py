from apps.backend.app.services.cross_encoder_reranker import CrossEncoderReranker


def test_reranker_fallback():
    r = CrossEncoderReranker()
    passages = ["The shop is open from 9 to 5.", "We accept appointments only."]
    out = r.rerank("what are your hours?", passages)
    assert isinstance(out, list)
    assert len(out) == len(passages)
    for p, s in out:
        assert isinstance(p, str)
        assert isinstance(s, float)
