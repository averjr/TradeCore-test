from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.models import User
from .serializers import UserSerializer, PostSerializer
from .models import Post


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True,
            methods=['GET'],
            name='User like this post')
    def like(self, request, pk=None):

        post = Post.objects.get(pk=pk)
        post.likes.add(self.request.user)
        post.save()
        serializer = self.get_serializer(post, many=False)
        return Response(serializer.data)

    @action(detail=True,
            methods=['GET'],
            name='User unlike this post')
    def unlike(self, request, pk=None):

        post = Post.objects.get(pk=pk)
        post.likes.remove(self.request.user)
        post.save()
        serializer = self.get_serializer(post, many=False)
        return Response(serializer.data)
