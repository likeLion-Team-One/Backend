import string
from rest_framework.serializers import ModelSerializer, ValidationError, CharField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser
from rest_framework.validators import UniqueValidator

class UserSerializer(ModelSerializer): 
    username = CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message='중복된 아이디입니다.')]
    )
    
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

# JWT 토큰 생성 시 사용자이름 추가
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
