from rest_framework import serializers
from .models import Like, Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "page", "content", "reply_to", "created_at", "updated_at"]
        read_only_fields = ["id", "page", "created_at", "updated_at"]

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post", "user_id"]
        read_only_fields = ["id", "user_id"]