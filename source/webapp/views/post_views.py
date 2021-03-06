from django.db.models import Q
from webapp.models import Post, PostVote
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from webapp.forms import SearchForm, PostForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.core.paginator import Paginator


class IndexView(ListView):
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = 3
    paginate_orphans = 0

    def get_queryset(self):
        data = Post.objects.all()
        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(title__icontains=search) | Q(author__username__icontains=search))
        return data.order_by('-date_create')


class CreatePostView(CreateView):
    template_name = 'posts/post_create'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect('webapp:post_view', pk=post.pk)


class PostView(DetailView):
    template_name = 'posts/post_view.html'
    model = Post
    paginate_comments_by = 2
    paginate_comments_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments, page, is_paginated = self.paginate_comments(self.object)
        context['comments'] = comments
        context['page_obj'] = page
        context['is_paginated'] = is_paginated

        return context

    def paginate_comments(self, post):
        comments = post.comments.all().order_by('-created_at')
        if comments.count() > 0:
            paginator = Paginator(comments, self.paginate_comments_by, orphans=self.paginate_comments_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)
            is_paginated = paginator.num_pages > 1  # page.has_other_pages()
            return page.object_list, page, is_paginated
        else:
            return comments, None, False


class PostUpdateView(UpdateView):
    template_name = 'posts/post_update.html'
    form_class = PostForm
    model = Post
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('webapp:post_view', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    template_name = 'posts/post_delete.html'
    model = Post
    success_url = reverse_lazy('webapp:index')


class PostVoteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        vote, created = PostVote.objects.get_or_create(post=post, user=request.user)
        if created:
            post.vote_amount += 1
            post.save()
            return HttpResponse(post.vote_amount)
        else:
            return HttpResponseForbidden()


class PostUnVoteView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        vote = get_object_or_404(post.votes, user=request.user)
        vote.delete()
        post.vote_amount -= 1
        post.save()
        return HttpResponse(post.vote_amount)

