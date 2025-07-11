from django.db import models
from django.conf import settings

class Post(models.Model):
    TYPE_CHOICES=(
        ('team_project','조별과제'),
        ('project','프로젝트'),
        ('competition','공모전'),
        ('supporters','서포터즈'),
        ('etc','기타')
    )
    FIELD_CHOICES=(
        ('planning','기획/아이디어'),
        ('design','디자인'),
        ('marketing','마케팅'),
        ('arts','예체능'),
        ('photography','사진/영상/UCC'),
        ('etc','기타')
    )
    STATUS_CHOICES = (
        ('draft', '임시저장'),
        ('published', '게시됨'),
    )
    STATUS_CHOICES = (
        ('draft', '임시저장'),
        ('published', '게시됨'),
    )
    title = models.CharField(max_length=200)
    project_type = models.TextField(verbose_name="프로젝트 유형", null=False, choices=TYPE_CHOICES, default="")
    project_field = models.TextField(verbose_name="프로젝트 분야", null=False, choices=FIELD_CHOICES, default="")
    target = models.TextField(verbose_name="프로젝트 대상",null=False, default="")
    start_date = models.DateField(verbose_name="프로젝트 시작일", null=False, blank=True)
    end_date = models.DateField(verbose_name="프로젝트 종료일", null=False, blank=True)
    host_org = models.TextField(verbose_name="주관기관", null=False, default="")
    description = models.TextField(verbose_name="프로젝트 설명", default="", null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_posts', null=True, blank=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    comment = models.CharField(verbose_name="댓글", max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
    
class ProjectBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'post')
    


