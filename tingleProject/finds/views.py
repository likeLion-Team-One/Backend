from .models import BookMark
from .serializers import FindsUserListSerializer, FindUserDetailSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from my.models import MyProfile
from groups.models import Team, TeamMember
from django.shortcuts import get_object_or_404

class FindUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MyProfile.objects.none()
    permission_classes = [IsAuthenticated] # 로그인한 사용자만

    def get_queryset(self):
        return MyProfile.objects.exclude(user=self.request.user) # 조회 - 내 프로필 제외
    
    def get_serializer_class(self):
        if self.action == 'retrieve': # 상세 조회일 때 
            return FindUserDetailSerializer
        return FindsUserListSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        total_users = queryset.count()
        return Response({
            "total_users": total_users,
            "profiles": serializer.data
        })
    
    # 그룹추가
    @action(detail=True, methods=['post'])
    def add_to_team(self, request, pk=None):
        profile = self.get_object()
        team = get_object_or_404(Team, id=request.data.get('team_id'))
        if TeamMember.objects.filter(team=team, user=profile.user).exists():
            return Response({'detail':'이미 팀에 속한 사용자입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        TeamMember.objects.create(team=team, user=profile.user)
        return Response({'detail': f'{profile.name}님이 팀({team.name})에 추가되었습니다.'}, status=status.HTTP_201_CREATED)
    
    #북마크 추가
    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        profile = self.get_object()
        bookmark_queryset = BookMark.objects.filter(user=request.user, profile=profile)
        if bookmark_queryset.exists():
            bookmark_queryset.delete()
            return Response({'detail': '북마크가 제거되었습니다.'}, status=status.HTTP_200_OK)
        BookMark.objects.create(user=request.user, profile=profile)
        return Response({'detail':'북마크가 추가되었습니다.'}, status=status.HTTP_201_CREATED)
    
    # 북마크 조회
    @action(detail=False, methods=['get'])
    def bookmark_list(self, request, pk=None):
        profile = MyProfile.objects.filter(bookmarks_by__user=request.user)
        serializer = FindsUserListSerializer(profile, many=True, context={'request': request})
        return Response({'count': profile.count(), 'bookmark_list': serializer.data})


