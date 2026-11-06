from drf_spectacular.utils import extend_schema
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .permissions import IsOwnerOrReadOnly
from .serializers import ProfileSerializer, PostWriteSerializer, PostReadSerializer
from instagram.models import Profile, Post


class ProfilesViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = (Profile.objects.filter(is_active=True)
                .select_related('user')
                .prefetch_related('comments', 'likes')
                )
    permission_classes = [IsOwnerOrReadOnly]


class PostsViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PostWriteSerializer
        return PostReadSerializer

    def get_queryset(self):
        return (Post.objects.filter(is_active=True)
                .select_related('user')
                .prefetch_related('comments', 'likes', 'images')
            )

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "user": {"type": "integer"},
                    "caption": {"type": "string"},
                    "images": {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    },
                },
                "required": ["user"],
            }
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "user": {"type": "integer"},
                    "caption": {"type": "string"},
                    "images": {
                        "type": "array",
                        "items": {"type": "string", "format": "binary"},
                    },
                },
                "required": ["user"],
            }
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)