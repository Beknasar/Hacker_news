from django.urls import path, include
from webapp.views import IndexView, CreatePostView, PostView, PostUpdateView, PostDeleteView, PostVoteView, \
    PostUnVoteView, CommentDeleteView, PostCommentCreateView, CommentUpdateView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('post/', include([
        path('add/', CreatePostView.as_view(), name='post_add'),
        path('<int:pk>/', include([
            path('', PostView.as_view(), name='post_view'),
            path('update/', PostUpdateView.as_view(), name='post_update'),
            path('delete/', PostDeleteView.as_view(), name='post_delete'),
            path('comments/add/', PostCommentCreateView.as_view(),
                 name='post_comment_add'),
            path('vote/', PostVoteView.as_view(), name='post_vote'),
            path('unvote/', PostUnVoteView.as_view(), name='post_unvote'),
        ])),
    ])),
    path('comment/', include([
        path('<int:pk>/', include([
            path('update/', CommentUpdateView.as_view(), name='comment_update'),
            path('delete/', CommentDeleteView.as_view(), name='comment_delete'),
        ]))
    ]))
]