from django.test import TestCase
import jwt
import pytest
from django.conf import settings
from rest_framework.test import APIClient
from pages.models import Page
from .models import Post

def make_token(user_id=101, role="USER"):
    return jwt.encode({"user_id": user_id, "role": role}, settings.JWT_SECRET_KEY, algorithm="HS256")

@pytest.mark.django_db
def test_only_owner_can_create_post():
    page = Page.objects.create(name="Owned Page", user_id=101)
    client = APIClient()
    token = make_token(user_id=205, role="USER")  # not the owner
    response = client.post(
        f"/page/{page.id}/post", {"content": "Hello"}, HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_owner_can_create_post():
    page = Page.objects.create(name="Owned Page", user_id=101)
    client = APIClient()
    token = make_token(user_id=101, role="USER")
    response = client.post(
        f"/page/{page.id}/post", {"content": "Hello"}, HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    assert response.status_code == 201

@pytest.mark.django_db
def test_admin_can_delete_any_post():
    page = Page.objects.create(name="Owned Page", user_id=101)
    post = Post.objects.create(page=page, content="Test")
    client = APIClient()
    token = make_token(user_id=999, role="ADMIN")
    response = client.delete(f"/post/{post.id}", HTTP_AUTHORIZATION=f"Bearer {token}")
    assert response.status_code == 204
