from django.shortcuts import render, get_object_or_404
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class TeamViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Team.objects.all()
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(created_by=user) 
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamListSerializer
        return TeamSerializer
    
    def perform_create(self, serializer):
        mode = self.request.query_params.get('mode', 'draft')
        team = serializer.save(
            created_by=self.request.user,
            status='draft' if mode == 'draft' else 'complete'
        )
        TeamMember.objects.get_or_create(team=team, user=self.request.user)
    
    def perform_update(self, serializer):
        mode = self.request.query_params.get('mode', 'complete')
        serializer.save(status='draft' if mode == 'draft' else 'complete')
    
    #팀 참여
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join(self, request, pk=None):
        team = get_object_or_404(Team, pk=pk)
        user = request.user

        if TeamMember.objects.filter(team=team, user=user).exists():
            return Response({'detail': '이미 참여 중인 팀입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        TeamMember.objects.create(team=team, user=user)
        return Response({'detail': '팀에 참여했습니다.'}, status=status.HTTP_200_OK)
    
    #팀 진행률 수정
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def progress(self, request, pk=None):
        team = get_object_or_404(Team, pk=pk)
        user = request.user

        if not TeamMember.objects.filter(team=team, user=user).exists():
            return Response({'detail': '팀 멤버만 진행률을 수정할 수 있습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        progress = request.data.get('progress')
        if progress is None:
            return Response({'detail': '진행률을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            progress = int(progress)
            if not 0 <= progress <= 100:
                raise ValueError
        except ValueError:
            return Response({'detail': '진행률은 0에서 100 사이의 정수여야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # Team의 progress 업데이트
        team = Team.objects.get(id=team.id)
        team.progress = progress
        team.save()

        return Response({'detail': '진행률이 수정되었습니다.'}, status=status.HTTP_200_OK)
    
    # 내 그룹
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_groups(self, request):
        user = request.user # 사용자
        # 내 그룹만 보여주기
        teams = Team.objects.filter(members__user=user).distinct()
        # 직렬화
        serializers = MyTeamSerializer(teams, many=True)
        return Response(serializers.data)


class TeamMemberViewSet(ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

    def perform_create(self, serializer):
        mode = self.request.query_params.get('mode', 'draft')
        team = serializer.save(
            created_by=self.request.user,
            status='draft' if mode == 'draft' else 'complete'
        )
        TeamMember.objects.get_or_create(team=team, user=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        team_id = self.kwargs.get("team_pk")  
        return Comment.objects.filter(team_id=team_id)

    def perform_create(self, serializer):
        team = get_object_or_404(Team, id=self.kwargs["team_pk"])
        serializer.save(user=self.request.user, team=team)

#북마크
class TeamBookmarkViewSet(ModelViewSet):
    serializer_class = TeamBookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TeamBookmark.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        team_id = request.data.get('team_id')
        if not team_id:
            return Response({'error': 'team_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)

        bookmark = TeamBookmark.objects.filter(user=user, team=team).first()
        if bookmark:
            bookmark.delete()
            return Response({'status': 'bookmark removed'})
        else:
            TeamBookmark.objects.create(user=user, team=team)
            return Response({'status': 'bookmark added'})