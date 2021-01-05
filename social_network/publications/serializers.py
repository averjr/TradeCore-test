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
        fields = ['username', 'email', 'posts', 'liked', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return


class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['title', 'body', 'owner', 'likes']
