import pytest


@pytest.mark.skip(reason="Wave 0 scaffold; implemented in later plans")
def test_create_tenant_required_fields() -> None:
    """ONB-01: creating a tenant requires complete business profile fields."""


@pytest.mark.skip(reason="Wave 0 scaffold; implemented in later plans")
def test_create_tenant_rejects_empty_services() -> None:
    """ONB-01/D-02: validation returns field-level errors for services."""
