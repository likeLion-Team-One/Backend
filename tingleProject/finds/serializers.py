from rest_framework import serializers
from my.models import MyProfile

# 사용자 리스트
class FindsUserListSerializer(serializers.ModelSerializer):
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
       model = MyProfile
       fields = ['name', 'job', 'is_bookmarked']

    def get_is_bookmarked(self, obj):
        user = self.context['request'].user
        return obj.bookmarks_by.filter(user=user).exists()

# 사용자 정보 세부사항
class FindUserDetailSerializer(serializers.ModelSerializer):
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = MyProfile
        exclude = ['user']
    
    def get_is_bookmarked(self, obj):
        user = self.context['request'].user
        return obj.bookmarks_by.filter(user=user).exists()

