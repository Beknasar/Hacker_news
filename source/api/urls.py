from django.urls import path, include

from api.views import get_token_view, PostCreateView

app_name = 'api_v1'


urlpatterns = [
    path('get_token/', get_token_view, name='get_token'),
    path('post_create/', PostCreateView.as_view(), name="post_create"),
]
