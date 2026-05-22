from app.services.knowledge import InMemoryVectorAdapter


def test_inmemory_adapter_indexes_and_queries():
    adapter = InMemoryVectorAdapter()
    tenant = "t-123"
    blocks = [
        "We offer haircuts and grooming services.",
        "Booking available on Mondays and Fridays.",
        "Call us for more details.",
    ]

    adapter.index_documents(tenant, blocks)

    results = adapter.query(tenant, "booking", top_k=2)
    assert isinstance(results, list)
    assert len(results) >= 1
    assert any("booking" in r.lower() for r in results)
