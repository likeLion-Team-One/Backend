from django.db import models
from django.conf import settings
from my.models import MyProfile

class BookMark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    profile = models.ForeignKey(MyProfile, on_delete=models.CASCADE, related_name='bookmarks_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'profile') #중복방지
        ordering = ['-created_at']
