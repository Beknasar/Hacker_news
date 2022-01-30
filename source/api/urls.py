from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import get_token_view, PostViewSet, UserViewSet

app_name = 'api_v1'

router = DefaultRouter()
router.register(r'post', PostViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('get_token/', get_token_view, name='get_token'),
    path('', include(router.urls)),
]
