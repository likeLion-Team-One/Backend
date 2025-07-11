from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, ProjectBookmarkViewSet


post_router = SimpleRouter(trailing_slash=False)
post_router.register('projects', PostViewSet, basename='projects')

comment_router = SimpleRouter(trailing_slash=False)
comment_router.register('comments', CommentViewSet, basename='comment')

bookmark_router = SimpleRouter()
bookmark_router.register('project_bookmark', ProjectBookmarkViewSet, basename='project_bookmark')
urlpatterns = [
    path('', include(post_router.urls)),
    path('projects/<int:post_id>/', include(comment_router.urls)),
    path('', include(bookmark_router.urls)),
]