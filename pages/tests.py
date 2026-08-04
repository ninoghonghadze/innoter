import jwt
import pytest
from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Page

def make_token(user_id=101, role="USER"):
    return jwt.encode(
        {"user_id": user_id, "role": role}, settings.JWT_SECRET_KEY, algorithm="HS256"
    )
@pytest.mark.django_db
def test_create_page_requires_auth():
    client = APIClient()
    response = client.post("/page", {"name": "Test Page"})
    assert response.status_code == 403

@pytest.mark.django_db
def test_create_page_success():
    client = APIClient()
    token = make_token()
    response = client.post(
        "/page", {"name": "Test Page"}, HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    assert response.status_code == 201
    assert response.data["user_id"] == 101


@pytest.mark.django_db
def test_non_owner_cannot_delete_page():
    page = Page.objects.create(name="Owned Page", user_id=101)
    client = APIClient()
    token = make_token(user_id=205, role="USER")
    response = client.delete(f"/page/{page.id}", HTTP_AUTHORIZATION=f"Bearer {token}")
    assert response.status_code == 403


@pytest.mark.django_db
def test_owner_can_delete_page():
    page = Page.objects.create(name="Owned Page", user_id=101)
    client = APIClient()
    token = make_token(user_id=101, role="USER")
    response = client.delete(f"/page/{page.id}", HTTP_AUTHORIZATION=f"Bearer {token}")
    assert response.status_code == 204
