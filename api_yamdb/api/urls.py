from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewsViewSet, TitleViewSet, UserViewSet, get_jwt_token,
                    signup)

v1_router = routers.DefaultRouter()

v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('users', UserViewSet, basename='users')

v1_review = v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet
)
v1_comment = v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', get_jwt_token),
]
