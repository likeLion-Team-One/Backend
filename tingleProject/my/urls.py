from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import *

my_router = SimpleRouter()
my_router.register('profile_update', MyProfileViewSet, basename='profile_update')

urlpatterns =[
    path('my_page/', MyPageViewSet.as_view(), name='my_page'),
    path('', include(my_router.urls)),
]