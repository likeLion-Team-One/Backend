from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FindUserViewSet

finds = DefaultRouter()
finds.register('finds', FindUserViewSet)

urlpatterns = [
    path('', include(finds.urls)),
]