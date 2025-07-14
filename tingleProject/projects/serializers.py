from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post, Comment, ProjectBookmark
from accounts.serializers import UserSerializer

class PostSerializer(ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['status', 'created_by']
    

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'post', 'user', 'created_at']
        read_only_fields = ['post']


class ProjectBookmarkSerializer(ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source='post',
        write_only=True
    )

    class Meta:
        model = ProjectBookmark
        fields = ['post', 'post_id']

