from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = models.Comment
        fields = ('id', 'post', 'content', 'user', 'user_id', 'created_at', 'updated_at', )


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        return models.Comment.objects.filter(post=obj).count()

    def get_likes(self, obj):
        return models.PostLike.objects.filter(post=obj).count()

    class Meta:
        model = models.Post
        fields = (
            'id', 'title', 'content', 'picture',
            'comment_count', 'comments', 'likes',
            'user', 'user_id', 'created_at', 'updated_at', 
        )

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostLike
        fields = ['id', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        User = get_user_model()
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
