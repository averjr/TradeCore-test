from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
                                    many=True,
                                    read_only=True,
                                    view_name='post-detail')
    liked = serializers.HyperlinkedRelatedField(
                                    many=True,
                                    read_only=True,
                                    view_name='post-detail'
    )

    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'posts', 'liked', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    liked_by = serializers.HyperlinkedRelatedField(
                                    many=True,
                                    read_only=True,
                                    view_name='user-detail')
                                    
    liked_by_me = serializers.ReadOnlyField(source='is_liked_by_me')

    class Meta:
        model = Post
        fields = ['pk', 'title', 'body', 'owner', 'liked_by', 'liked_by_me']
