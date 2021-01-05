from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.models import User
from .serializers import UserSerializer, PostSerializer
from .models import Post
from .permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True,
            methods=['GET'],
            name='User like this post')
    def like(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        post.liked_by.add(self.request.user)
        post.save()
        serializer = self.get_serializer(post, many=False)
        return Response(serializer.data)

    @action(detail=True,
            methods=['GET'],
            name='User unlike this post')
    def unlike(self, request, pk=None):

        post = Post.objects.get(pk=pk)
        post.liked_by.remove(self.request.user)
        post.save()
        serializer = self.get_serializer(post, many=False)
        return Response(serializer.data)
