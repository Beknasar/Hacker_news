from api.permissions import GETModelPermissions
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.http import HttpResponse, HttpResponseNotAllowed
from rest_framework.viewsets import ViewSet, ModelViewSet
from django.views.decorators.csrf import ensure_csrf_cookie
from webapp.models import Post, PostVote
from api.serializers import UserSerializer, PostSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class PostViewSet(ViewSet):
    queryset = Post.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # self.request.method == "GET"
            return [GETModelPermissions()]
        else:
            return [AllowAny()]

    def list(self, request):
        objects = Post.objects.all()
        slr = PostSerializer(objects, many=True, context={'request': request})
        return Response(slr.data)

    def create(self, request):
        slr = PostSerializer(data=request.data, context={'request': request})
        if slr.is_valid():
            post = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        slr = PostSerializer(post, context={'request': request})
        return Response(slr.data)

    def update(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        slr = PostSerializer(data=request.data, instance=post, context={'request': request})
        if slr.is_valid():
            post = slr.save()
            return Response(slr.data)
        else:
            return Response(slr.errors, status=400)

    def destroy(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response({'pk': pk})

    @action(methods=['post'], detail=True)
    def vote(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        vote, created = PostVote.objects.get_or_create(post=post, user=request.user)
        if created:
            post.vote_amount += 1
            post.save()
            return Response({'pk': pk, 'votes': post.vote_amount})
        else:
            return Response(status=403)

    @action(methods=['delete'], detail=True)
    def unvote(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        like = get_object_or_404(post.votes, user=request.user)
        like.delete()
        post.vote_amount -= 1
        post.save()
        return Response({'pk': pk, 'votes': post.vote_amount})


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer