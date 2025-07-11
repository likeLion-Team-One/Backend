from django.db import models
from django.contrib.auth import get_user_model

class MyProfile(models.Model):
    GENDER_CHOICES = [
        ('male', '남성'),
        ('female', '여성'),
    ]
    REGION_CHOICES = [
        ('seoul', '서울특별시'),
        ('busan', '부산광역시'),
        ('incheon', '인천광역시'),
        ('daegu', '대구광역시'),
        ('daejeon', '대전광역시'),
        ('gwangju', '광주광역시'),
        ('ulsan', '울산광역시'),
        ('sejong', '세종특별자치시'),
        ('gyeonggi', '경기도'),
        ('chungbuk', '충청북도'),
        ('chungnam', '충청남도'),
        ('jeonnam', '전라남도'),
        ('gyeongbuk', '경상북도'),
        ('gyeongnam', '경상남도'),
        ('gangwon', '강원특별자치도'),
        ('jeonbuk', '전북특별자치도'),
        ('jeju', '제주특별자치도'),
    ]
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=20)
    age = models.PositiveIntegerField(default=20)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    region = models.CharField(max_length=30, choices=REGION_CHOICES)
    district = models.CharField(max_length=30, blank=True)
    job = models.CharField(max_length=50) 
    education = models.CharField(max_length=30, blank=True, null=True)
    major = models.CharField(max_length=30, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.gender}), {self.job}"


