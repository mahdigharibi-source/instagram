from rest_framework.routers import DefaultRouter
from .views import ProfilesViewSet
router = DefaultRouter()
router.register('profiles', ProfilesViewSet, basename='profiles')

urlpatterns = []

urlpatterns += router.urls