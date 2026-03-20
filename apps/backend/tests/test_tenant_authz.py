import pytest


@pytest.mark.skip(reason="Wave 0 scaffold; implemented in later plans")
def test_owner_token_required() -> None:
    """SEC-01: protected owner endpoint returns 401 when token is missing."""


@pytest.mark.skip(reason="Wave 0 scaffold; implemented in later plans")
def test_cross_tenant_forbidden() -> None:
    """SEC-01: token bound to another tenant is denied with 403."""
