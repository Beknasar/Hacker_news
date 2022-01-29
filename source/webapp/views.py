from django.db.models import Q
from webapp.models import Post
from django.views.generic import ListView, CreateView
from webapp.forms import SearchForm, PostForm
from django.urls import reverse, reverse_lazy


class IndexView(ListView):
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = 7
    paginate_orphans = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        form = SearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        kwargs['form'] = form
        return super().get_context_data(object_list=object_list, **kwargs)

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

    def get_success_url(self):
        return reverse('webapp:index')
        # return reverse('post_view', kwargs={'pk': self.object.pk})