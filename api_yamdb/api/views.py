from rest_framework import viewsets
from rest_framework import permissions

from yamdb.models import Review, Comment
from .permissions import GetPermissionsReview
from .serializer import CommentSerializer, ReviewSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [GetPermissionsReview, permissions.IsAdminUser]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
