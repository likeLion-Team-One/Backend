from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
from rest_framework_simplejwt.views import ( 
    #TokenObtainPairView, 
    TokenRefreshView,
)
from .views import MyTokenObtainPairView

user_router = SimpleRouter()
user_router.register('user', views.UserViewSet)

urlpatterns =[
    path('', include(user_router.urls)),
    path('auth/', include('rest_framework.urls')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]