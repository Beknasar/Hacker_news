from django.urls import path, include
from webapp.views import IndexView, CreatePostView, PostView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('post/', include([
        path('add/', CreatePostView.as_view(), name='post_add'),
        path('<int:pk>/', PostView.as_view(), name='post_view'),
    ])),
]