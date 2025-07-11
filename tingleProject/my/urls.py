from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import MyProfileViewSet

my_router = SimpleRouter()
my_router.register('profile_update', MyProfileViewSet)

urlpatterns =[
    path('', include(my_router.urls)),
]