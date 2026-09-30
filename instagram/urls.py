from rest_framework.routers import DefaultRouter
from .views import ProfilesViewSet, PostViewSet
router = DefaultRouter()
router.register('profiles', ProfilesViewSet, basename='profiles')
router.register('posts', PostViewSet, basename='posts')

urlpatterns = []

urlpatterns += router.urls