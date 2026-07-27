from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from authentication.permissions import IsAdminOrModeratorOrOwner, IsAuthenticated
from pages.models import Page
from .models import Post
from .serializers import PostSerializer

class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        page = Page.objects.get(id=self.kwargs["page_id"])
        if page.user_id != self.request.user.get("user_id"):
            raise PermissionDenied("Only the page owner can post")
        serializer.save(page=page)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = "post_id"
    permission_classes = [IsAuthenticated, IsAdminOrModeratorOrOwner]