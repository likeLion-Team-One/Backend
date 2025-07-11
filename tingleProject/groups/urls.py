from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from django.urls import path, include
from .views import TeamViewSet, CommentViewSet, TeamBookmarkViewSet, TeamMemberViewSet

team_router = SimpleRouter(trailing_slash=False)
team_router.register('teams', TeamViewSet, basename='teams')

comment_router = NestedSimpleRouter(team_router, 'teams', lookup='team')
comment_router.register('comments', CommentViewSet, basename='team-comments')

member_router = NestedSimpleRouter(team_router, 'teams', lookup='team')
member_router.register('members', TeamMemberViewSet, basename='team-members')

bookmark_router = SimpleRouter()
bookmark_router.register('team_bookmark', TeamBookmarkViewSet, basename='team_bookmark')


urlpatterns = [
    path('', include(team_router.urls)),
    path('', include(comment_router.urls)),
    path('', include(member_router.urls)),
    path('', include(bookmark_router.urls)),
]
