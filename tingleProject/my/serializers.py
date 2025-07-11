from rest_framework.serializers import ModelSerializer
from .models import MyProfile

class MyProfileSerializer(ModelSerializer):
    class Meta:
        model = MyProfile
        fields = [
            'id', 'name', 'age', 'gender', 'region', 'district',
            'job','education', 'major', 'detail',
        ]
