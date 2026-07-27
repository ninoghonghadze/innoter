from django.urls import path
from .views import PostCreateView, PostDetailView

urlpatterns = [
    path("page/<int:page_id>/post", PostCreateView.as_view(), name="post-create"),
    path("post/<int:post_id>", PostDetailView.as_view(), name="post-detail"),
]