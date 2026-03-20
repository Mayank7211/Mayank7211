import pytest


@pytest.mark.skip(reason="Wave 0 scaffold; implemented in later plans")
def test_allowed_origin_receives_cors_headers() -> None:
    """SEC-02: allowlisted origin gets expected CORS headers."""


@pytest.mark.skip(reason="Wave 0 scaffold; implemented in later plans")
def test_disallowed_origin_blocked() -> None:
    """SEC-02: disallowed origins are not granted credentialed CORS access."""
