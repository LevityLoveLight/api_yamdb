from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from users.views import email, get_jwt_token

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
    path('v1/auth/email/', email),
    path('v1/auth/token/', get_jwt_token),
]
