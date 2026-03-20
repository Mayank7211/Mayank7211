import pytest


@pytest.mark.skip(reason="Wave 0 scaffold; implemented in later plans")
def test_chat_and_upload_rate_limited() -> None:
    """SEC-03: chat/upload return deterministic 429 payload contract."""
