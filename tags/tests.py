from django.test import TestCase
import jwt
import pytest
from django.conf import settings
from rest_framework.test import APIClient
from .models import Tag

def make_token(user_id=101, role="USER"):
    return jwt.encode({"user_id": user_id, "role": role}, settings.JWT_SECRET_KEY, algorithm="HS256")

@pytest.mark.django_db
def test_create_tag():
    client = APIClient()
    token = make_token()
    response = client.post("/tag", {"name": "nature"}, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert response.status_code == 201

@pytest.mark.django_db
def test_filter_tags_by_name():
    Tag.objects.create(name="nature")
    Tag.objects.create(name="travel")
    client = APIClient()
    token = make_token()
    response = client.get("/tags?filter_by_name=nat", HTTP_AUTHORIZATION=f"Bearer {token}")
    assert response.status_code == 200
    assert len(response.data) == 1
