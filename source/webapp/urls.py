from django.urls import path, include
from webapp.views import IndexView, CreatePostView, PostView, PostUpdateView, PostDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('post/', include([
        path('add/', CreatePostView.as_view(), name='post_add'),
        path('<int:pk>/', include([
            path('', PostView.as_view(), name='post_view'),
            path('update/', PostUpdateView.as_view(), name='post_update'),
            path('delete/', PostDeleteView.as_view(), name='post_delete'),
        ])),
    ])),
]