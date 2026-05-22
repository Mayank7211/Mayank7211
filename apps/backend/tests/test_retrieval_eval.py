import os
import json
from tools.retrieval_eval import run_evaluation


def test_run_evaluation_smoke(tmp_path, monkeypatch):
    fixtures = tmp_path / "fixtures.json"
    data = [
        {"query": "opening hours", "relevant": ["We are open Monday to Friday from 9am to 6pm."]}
    ]
    fixtures.write_text(json.dumps(data))

    # Ensure default_vector_adapter has some data
    from app.services.knowledge import default_vector_adapter
    default_vector_adapter.index_documents("test-tenant", ["We are open Monday to Friday from 9am to 6pm."])

    # Run evaluation (should not raise)
    run_evaluation(str(fixtures), k=1)
