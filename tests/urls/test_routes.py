import pytest
from django.urls import resolve, reverse


@pytest.mark.parametrize(
    "name,expected",
    [
        ("api-v1:categories-list", "/api/v1/categories/"),
        ("api-v1:services-list", "/api/v1/services/"),
        ("api-auth:login", "/api/v1/auth/login/"),
        ("api-auth:me", "/api/v1/auth/me/"),
    ],
)
def test_reverse_new_routes(name, expected):
    assert reverse(name) == expected


def test_categories_route_resolves_viewset():
    match = resolve("/api/v1/categories/")
    assert match.view_name == "api-v1:categories-list"
    assert match.func.cls.__name__.lower().startswith("category")


@pytest.mark.parametrize(
    "legacy_path,target,status",
    [
        ("/api/categories/", "/api/v1/categories/", 301),
        ("/auth/login/", "/api/v1/auth/login/", 308),
    ],
)
def test_legacy_redirects(client, legacy_path, target, status):
    response = client.get(legacy_path, follow=False)
    assert response.status_code == status
    assert response.headers["Location"].startswith(target)


def test_healthz(client):
    response = client.get("/healthz/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
