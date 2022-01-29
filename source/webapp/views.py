from django.db.models import Q
from webapp.models import Post
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from webapp.forms import SearchForm, PostForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect


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
                data = data.filter(Q(title__icontains=search) | Q(author__icontains=search))
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

