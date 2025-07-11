from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post, Comment, ProjectBookmark

class PostSerializer(ModelSerializer):
    
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
    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source='post',        # 내부에서는 post 필드로 매핑
        write_only=True       # 입력 시에만 쓰고, 출력에는 안 보임
    )
    class Meta:
        model = ProjectBookmark
        fields = ['id', 'user', 'post', 'post_id']
        read_only_fields = ['id', 'user', 'post']

