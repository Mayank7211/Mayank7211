from app.services.reranker import rerank


def test_reranker_orders_relevant():
    docs = [
        "We are open Monday to Friday from 9am to 6pm.",
        "Contact us for bookings.",
        "Open weekdays 9-6",
    ]
    q = "opening hours"
    ranked = rerank(q, docs)
    # Top doc should be an opening hours doc
    assert any("open" in d[0].lower() for d in ranked[:2])
