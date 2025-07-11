from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Team, TeamMember, Comment, TeamBookmark
from projects.models import Post

User = get_user_model()

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'project_type', 'project_field']

class BaseTeamProjectInfoSerializer(ModelSerializer):
    project_type = SerializerMethodField()
    project_field = SerializerMethodField()

    def get_project_type(self, obj):
        if obj.project:
            return obj.project.get_project_type_display()
        return None

    def get_project_field(self, obj):
        if obj.project:
            return obj.project.get_project_field_display()
        return None
    
    
class TeamMemberSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)  # 중첩 serializer 사용
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    
    class Meta:
        model = TeamMember
        fields = ['id', 'team', 'user', 'user_id']
        read_only_fields = ['id', 'team']


class TeamSerializer(BaseTeamProjectInfoSerializer):
    project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source='project',
        write_only=True  # 요청 시만 사용 (입력 전용)
    )

    target = SerializerMethodField()
    members = TeamMemberSerializer(many=True, read_only=True)  # 중첩 serializer 사용
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Team # Group 모델을 참조
        fields = ['id', 'name', 'project', 'project_id', 'project_type', 'project_field', 'target', 'part', 'description', 'members', 'progress', 'created_by']
        read_only_fields = ['id', 'status', 'created_by'] 

    
    def get_target(self, obj):
        if obj.project:
            return obj.project.target
        return None



class TeamListSerializer(BaseTeamProjectInfoSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'project', 'project_type', 'project_field', 'created_by']
        read_only_fields = ['id', 'status']

#댓글
class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment  
        fields = ['id', 'comment', 'user', 'team', 'created_at']
        read_only_fields = ['id', 'user', 'team', 'created_at']

#북마크
class TeamBookmarkSerializer(serializers.ModelSerializer):
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='team',
        write_only=True
    )

    class Meta:
        model = TeamBookmark
        fields = ['id', 'user', 'team', 'team_id']
        read_only_fields = ['id', 'user', 'team']