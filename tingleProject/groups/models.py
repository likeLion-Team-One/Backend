from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Post
# Create your models here.

User = get_user_model()

class Team(models.Model):
    STATUS_CHOICES = (
        ('draft', '임시저장'),
        ('published', '게시됨'),
    )
    STATUS_CHOICES = (
        ('draft', '임시저장'),
        ('published', '게시됨'),
    )
    name = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
    part = models.CharField(max_length=50)
    description = models.TextField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    progress = models.PositiveIntegerField(default=0) # 진행률 (0-100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams', null=True)

    def __str__(self):
        return self.name
    
class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('team', 'user')


class Comment(models.Model):
    comment = models.CharField(verbose_name="댓글", max_length=200)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='team_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
    

#북마크
class TeamBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_bookmarks')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_bookmarks')

    class Meta:
        unique_together = ('user', 'team')

    

