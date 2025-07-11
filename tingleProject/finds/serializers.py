from rest_framework import serializers
from my.models import MyProfile

# 사용자 리스트
class FindsUserListSerializer(serializers.ModelSerializer):
    total_user = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
       model = MyProfile
       fields = ['id', 'name', 'job', 'total_user', 'is_bookmarked']

    def get_total_user(self, obj):
        return MyProfile.objects.exclude(user=self.context['request'].user).count()

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
        return obj.bookmarks_by.filter(user=user).exist()

