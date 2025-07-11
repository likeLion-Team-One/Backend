import string
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser

class UserSerializer(ModelSerializer): 
    # 중복아이디 검사
    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise ValidationError('중복된 아이디입니다.')
        return value
    
    # 비밀번호 유효성 검사
    def validate_password(self, value):
        if(
            len(value) < 8 or
            not any(c.isalpha() for c in value) or
            not any(c.isdigit() for c in value) or
            not any(c in string.punctuation for c in value)
        ): 
            raise ValidationError('비밀번호 양식이 틀립니다.')
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
        
    class Meta:
        model = CustomUser
        fields = ['name', 'username', 'password', 'phone', 'email']
        # extra_kwargs = {
        #     'password': {'write_only': True},
        # }

# 사용자이름
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
