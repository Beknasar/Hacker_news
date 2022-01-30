from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from webapp.models import Comment, Post
from webapp.forms import PostCommentForm


class PostCommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comment/comment_create.html'
    form_class = PostCommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.save()
        return redirect('webapp:post_view', pk=post.pk)


class CommentDeleteView(DeleteView):
    model = Comment
    permission_required = 'webapp.delete_comment'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:post_view', kwargs={'pk': self.object.post.pk})
