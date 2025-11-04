"""Integration smoke tests for top-level routing and redirects."""
import pytest
from django.urls import resolve
from rest_framework.test import APIClient

from Category.models import ModelCategory


def _resolved_view_name(path: str) -> str:
    match = resolve(path)
    if hasattr(match.func, "view_class"):
        return match.func.view_class.__name__
    if hasattr(match.func, "cls"):
        return match.func.cls.__name__
    return match.func.__name__


def test_login_route_resolves():
    assert _resolved_view_name("/api/v1/auth/login/") == "KnoxLoginView"


def test_services_router_resolves():
    assert _resolved_view_name("/api/v1/services/") == "ServicePostViewSet"


def test_profile_certifications_resolves():
    assert _resolved_view_name("/api/v1/profile/certifications/") == "Kompetenser_intygsListAPIView"


@pytest.mark.django_db
def test_categories_list_returns_data_or_auth_response():
    ModelCategory.objects.create(name="Tech", description="Services for tech")
    client = APIClient()
    response = client.get("/api/v1/categories/")
    assert response.status_code in {200, 401, 403}
    assert response.status_code != 404


def test_legacy_auth_redirects_to_v1():
    client = APIClient()
    response = client.get("/auth/login/")
    assert response.status_code == 308
    assert response.headers["Location"] == "/api/v1/auth/login/"


def test_legacy_service_list_redirects():
    client = APIClient()
    response = client.get("/api/service/list")
    assert response.status_code == 308
    assert response.headers["Location"] == "/api/v1/services/"


def test_healthz_returns_ok_payload():
    client = APIClient()
    response = client.get("/healthz/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
