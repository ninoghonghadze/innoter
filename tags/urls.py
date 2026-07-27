from django.urls import path
from .views import TagListCreateView

urlpatterns = [
    path("tag", TagListCreateView.as_view(), name="tag-create"),
    path("tags", TagListCreateView.as_view(), name="tag-list"),
]