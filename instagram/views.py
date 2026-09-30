from rest_framework.viewsets import ModelViewSet
from .serializers import ProfileSerializer, PostSerializer
from instagram.models import Profile, Post


class ProfilesViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = (Profile.objects.filter(is_active=True)
                .select_related('user')
                .prefetch_related('comments', 'likes')
                )


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = (Post.objects.filter(is_active=True)
                .select_related('user__user')
                .prefetch_related('comments', 'likes', 'images')
                )
