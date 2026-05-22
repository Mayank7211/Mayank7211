from app.core.config import settings


def test_allowed_origin_receives_cors_headers(client) -> None:
    origin = settings.allowed_cors_origins[0]
    response = client.options(
        "/api/chat",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == origin
    assert response.headers.get("access-control-allow-credentials") == "true"


def test_disallowed_origin_blocked(client) -> None:
    response = client.options(
        "/api/chat",
        headers={
            "Origin": "https://evil.example",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 400
    assert response.headers.get("access-control-allow-origin") is None
