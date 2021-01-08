from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post
from .helpers import is_existent_email, get_clearbit_data


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
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': True}}

    def validate_email(self, value):
        # FIXME: dirty hack to pass email validation when call fom bot
        if 'from_bot' in self.context['request'].data:
            return value

        if not is_existent_email(value):
            raise serializers.ValidationError("Non existent email")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')

        # TODO: move following to the proper place to validate incoming data
        additional_user_data = get_clearbit_data(validated_data['email'])
        # change to z = x | y  if pyhton 3.9+
        validated_data = {**validated_data, **additional_user_data}

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
