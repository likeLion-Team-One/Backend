from .models import MyProfile
from .serializers import MyProfileSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

# 마이페이지
class MyPageViewSet(APIView):
    permission_classes = [IsAuthenticated] # 로그인한 사용자만

    def get(self, request):
        user = request.user
        return Response({"name":user.name})


# 프로필 업데이트
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
    