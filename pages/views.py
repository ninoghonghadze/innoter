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
        serializer.save(
            user_id=self.request.user.get("user_id"),
            group_id=self.request.user.get("group_id"),
        )
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        page = Page.objects.filter(id=self.kwargs["page_id"]).first()
        if not page:
            raise NotFound("Page not found")
        role = self.request.user.get("role")
        user_id = self.request.user.get("user_id")
        group_id = self.request.user.get("group_id")

        is_admin = role == "ADMIN"
        is_moderator_same_group = role == "MODERATOR" and group_id == page.group_id
        is_owner = page.user_id == user_id

        if not (is_admin or is_moderator_same_group or is_owner):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Not allowed to view followers")
        return Follower.objects.filter(page_id=page.id)

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
        page = Page.objects.filter(id=page_id).first()
        if not page:
            raise NotFound("Page not found")

        is_admin = role == "ADMIN"
        is_moderator_same_group = role == "MODERATOR" and request.user.get("group_id") == page.group_id

        if not (is_admin or is_moderator_same_group):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only Admin or same-group Moderator can block a page")

        unblock_date = request.data.get("unblock_date")
        page.is_blocked = True
        page.unblock_date = unblock_date
        page.save()
        return Response({"detail": "Page blocked", "unblock_date": unblock_date}, status=200)
        
class PageAddTagsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, page_id):
        page = Page.objects.filter(id=page_id).first()
        if not page:
            raise NotFound("Page not found")
        if page.user_id != request.user.get("user_id"):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only the page owner can add tags")

        tag_ids = request.data.get("tags", [])
        from tags.models import Tag
        valid_tags = Tag.objects.filter(id__in=tag_ids)
        page.tags.add(*valid_tags)

        return Response(PageSerializer(page).data, status=200)