import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "innotter.settings")
django.setup()

import jwt
from django.conf import settings

owner_token = jwt.encode(
    {"user_id": 101, "role": "USER"}, settings.JWT_SECRET_KEY, algorithm="HS256"
)

other_user_token = jwt.encode(
    {"user_id": 205, "role": "USER"}, settings.JWT_SECRET_KEY, algorithm="HS256"
)

print("Owner token (101):")
print(owner_token)
print()
print("Other user token (205):")
print(other_user_token)


# docker compose exec web uv run python -m authentication.demo_tokens
