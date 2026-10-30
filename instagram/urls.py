from rest_framework.routers import DefaultRouter
from .views import ProfilesViewSet, PostsViewSet
router = DefaultRouter()
router.register('profiles', ProfilesViewSet, basename='profiles')
router.register('posts', PostsViewSet, basename='posts')

urlpatterns = []

urlpatterns += router.urls