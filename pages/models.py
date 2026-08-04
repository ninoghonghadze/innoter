from django.db import models


class Page(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user_id = models.PositiveIntegerField()
    group_id = models.PositiveIntegerField(null=True, blank=True)
    image_url = models.URLField(blank=True)
    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField("tags.Tag")


class Follower(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    user_id = models.PositiveIntegerField()
