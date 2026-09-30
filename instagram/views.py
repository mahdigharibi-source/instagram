
from rest_framework.viewsets import ModelViewSet
from .serializers import ProfileSerializer
from instagram.models import Profile


class ProfilesViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer