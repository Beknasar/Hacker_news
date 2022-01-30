import json
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.views .generic import View
from django.views.decorators.csrf import ensure_csrf_cookie
from webapp.models import Post


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class PostCreateView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            response = JsonResponse({
                'error': 'Forbidden'
            })
            response.status_code = 403
            return response
        data = json.loads(request.body)
        print(data)
        post = Post.objects.create(
            author=self.request.user,
            title=data['title'],
            link=data['link']
        )
        return JsonResponse({
            'pk': post.pk,
            'author_id': post.author_id,
            'title': post.title,
            'link': post.link,
            'date_create': post.date_create
        })

