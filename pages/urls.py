from django.urls import path
from .views import (BlockPageView, FeedView, FollowPageView, PageAddTagsView,
                    PageDetailView, PageFollowersView, PageListCreateView,
                    UnfollowPageView, PageImageUploadView)
urlpatterns = [
    path("page", PageListCreateView.as_view(), name="page-list-create"),
    path("page/<int:page_id>", PageDetailView.as_view(), name="page-detail"),
    path("page/<int:page_id>/follow", FollowPageView.as_view(), name="page-follow"),
    path(
        "page/<int:page_id>/unfollow", UnfollowPageView.as_view(), name="page-unfollow"
    ),
    path(
        "page/<int:page_id>/followers",
        PageFollowersView.as_view(),
        name="page-followers",
    ),
    path("feed", FeedView.as_view(), name="feed"),
    path("page/<int:page_id>/block", BlockPageView.as_view(), name="page-block"),
    path("page/<int:page_id>/tags", PageAddTagsView.as_view(), name="page-add-tags"),
    path("page/<int:page_id>/upload-image", PageImageUploadView.as_view(), name="page-upload-image"),
]
