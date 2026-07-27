from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from authentication.permissions import (IsAdminOrModeratorOrOwner,
                                        IsAuthenticated, IsPageOwner)
from posts.serializers import PostSerializer
from .models import Follower, Page
from .serializers import FollowerSerializer, PageSerializer
from datetime import datetime
from authentication.permissions import IsAdmin, IsModerator


class PageListCreateView(generics.ListCreateAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.get("user_id"))


class PageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    lookup_url_kwarg = "page_id"

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsAdminOrModeratorOrOwner()]
        if self.request.method == "PATCH":
            return [IsAuthenticated(), IsPageOwner()]
        return [IsAuthenticated()]


class FollowPageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, page_id):
        page = Page.objects.filter(id=page_id).first()
        if not page:
            raise NotFound("Page not found")
        Follower.objects.get_or_create(page=page, user_id=request.user.get("user_id"))
        return Response({"detail": "Followed"}, status=200)


class UnfollowPageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, page_id):
        Follower.objects.filter(
            page_id=page_id, user_id=request.user.get("user_id")
        ).delete()
        return Response({"detail": "Unfollowed"}, status=200)


class PageFollowersView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated, IsAdminOrModeratorOrOwner]

    def get_queryset(self):
        return Follower.objects.filter(page_id=self.kwargs["page_id"])


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from posts.models import Post

        followed_page_ids = Follower.objects.filter(
            user_id=self.request.user.get("user_id")
        ).values_list("page_id", flat=True)
        return Post.objects.filter(page_id__in=followed_page_ids).order_by(
            "-created_at"
        )

class BlockPageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, page_id):
        role = request.user.get("role")
        if role not in ("ADMIN", "MODERATOR"):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only Admin or Moderator can block a page")
        page = Page.objects.filter(id=page_id).first()
        if not page:
            raise NotFound("Page not found")
        unblock_date = request.data.get("unblock_date")
        page.is_blocked = True
        page.unblock_date = unblock_date
        page.save()
        return Response({"detail": "Page blocked", "unblock_date": unblock_date}, status=200)