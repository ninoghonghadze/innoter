from django.urls import path
from .views import (
    FollowPageView,
    PageDetailView,
    PageFollowersView,
    PageListCreateView,
    UnfollowPageView,
)

urlpatterns = [
    path("page", PageListCreateView.as_view(), name="page-list-create"),
    path("page/<int:page_id>", PageDetailView.as_view(), name="page-detail"),
    path("page/<int:page_id>/follow", FollowPageView.as_view(), name="page-follow"),
    path("page/<int:page_id>/unfollow", UnfollowPageView.as_view(), name="page-unfollow"),
    path("page/<int:page_id>/followers", PageFollowersView.as_view(), name="page-followers"),
]