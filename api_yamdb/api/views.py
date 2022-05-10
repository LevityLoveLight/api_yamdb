from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions

from yamdb.models import Review, Comment, User
from .permissions import ReviewPermissions
from .serializer import CommentSerializer, ReviewSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermissions,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ReviewPermissions,)

    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id')
        post = get_object_or_404(Comment, pk=comment_id )
        return post.comments.filter(post_id=comment_id )

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user.username)
        serializer.save(author=user)

