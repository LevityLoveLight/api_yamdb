from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.urls import include, path
from rest_framework import routers

from .views import ReviewsViewSet, CommentViewSet

v1_router = routers.DefaultRouter()

v1_review = v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet
)
v1_comment = v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet
)


urlpatterns = [
    path('v1/', include('v1_router.urls'))
]
