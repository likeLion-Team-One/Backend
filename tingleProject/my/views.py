from .models import MyProfile
from .serializers import MyProfileSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

class MyProfileViewSet(ModelViewSet):
    queryset = MyProfile.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = [IsAuthenticated] # 로그인한 사용자만 수정

    def perform_create(self, serializer):
        user = self.request.user
        if MyProfile.objects.filter(user=user).exists():
            raise ValidationError({"detail": "이미 프로필이 존재합니다."})
        serializer.save(user=user)

    def get_queryset(self):
        return MyProfile.objects.filter(user=self.request.user)
    