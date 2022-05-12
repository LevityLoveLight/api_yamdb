from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewsViewSet,
                    TitleViewSet, UserViewSet, email, get_jwt_token)

v1_router = routers.DefaultRouter()

v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(r'users', UserViewSet, basename='users')

v1_review = v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet
)
v1_comment = v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/email/', email),
    path('v1/auth/token/', get_jwt_token),
]
