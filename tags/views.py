from rest_framework import generics

from authentication.permissions import IsAuthenticated

from .models import Tag
from .serializers import TagSerializer


class TagListCreateView(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Tag.objects.all()
        name_filter = self.request.query_params.get("filter_by_name")
        if name_filter:
            queryset = queryset.filter(name__icontains=name_filter)
        return queryset
