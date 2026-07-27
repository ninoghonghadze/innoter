from django.db import models

from pages.models import Page


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.TextField()
    reply_to = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.PositiveIntegerField()
