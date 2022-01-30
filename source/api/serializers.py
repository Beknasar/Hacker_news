from rest_framework import serializers
from webapp.models import Post
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True, view_name='api_v1:user-detail')
    class Meta:
        model = get_user_model()
        fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email']


class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(read_only=True,
                                               view_name='api:post-detail')
    author_url = serializers.HyperlinkedRelatedField(read_only=True, source='author',
                                                     view_name='api:user-detail')
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'url', 'title', 'link', 'author', 'author_url', 'date_create']
        read_only_fields = ('author',)