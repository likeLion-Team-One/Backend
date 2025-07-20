from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import MyProfile

class MyProfileSerializer(ModelSerializer):
    region =SerializerMethodField()

    class Meta:
        model = MyProfile
        fields = [
            'id', 'name', 'age', 'gender', 'region', 'district',
            'job','education', 'major', 'detail',
        ]
    
    def get_region(self, obj):
        return obj.get_region_display()
