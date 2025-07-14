from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment, ProjectBookmark
from .serializers import PostSerializer, CommentSerializer, ProjectBookmarkSerializer
from rest_framework.viewsets import ModelViewSet

class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        # queryset = Post.objects.filter(created_by = self.request.user)
        queryset = Post.objects.filter() # 전체 가져오기 
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset
    
    def perform_create(self, serializer):
        mode = self.request.query_params.get("mode", "draft")
        serializer.save(
            created_by=self.request.user,
            status='draft' if mode == 'draft' else 'complete'
        
        )

    def perform_update(self, serializer):
        mode = self.request.query_params.get("mode", "complete")
        serializer.save(status='draft' if mode == 'draft' else 'complete')

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    
    def get_queryset(self, **kwargs):
        id = self.kwargs['post_id']
        return self.queryset.filter(post=id)
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')  # URL에서 /projects/<pk>/comments
        post = Post.objects.get(pk=post_id)
        serializer.save(user=self.request.user, post=post)  
    
#bookmark
class ProjectBookmarkViewSet(ModelViewSet):
    serializer_class = ProjectBookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProjectBookmark.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        post = serializer.validated_data['post']

    # 토글
        bookmark = ProjectBookmark.objects.filter(user=user, post=post).first()
        if bookmark:
            bookmark.delete()
            return Response({'status': 'bookmark removed'})
        else:
            ProjectBookmark.objects.create(user=user, post=post)
            return Response({'status': 'bookmark added'})

        
        