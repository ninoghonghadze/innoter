from rest_framework import serializers
from .models import Follower, Page
from tags.models import Tag
class PageSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)
    class Meta:
        model = Page
        fields = [
            "id",
            "name",
            "description",
            "user_id",
            "image_url",
            "is_blocked",
            "unblock_date",
            "tags",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user_id", "is_blocked", "unblock_date", "tags", "created_at", "updated_at"]

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ["id", "page", "user_id"]
        read_only_fields = ["id", "user_id"]