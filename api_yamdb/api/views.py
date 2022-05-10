from django.db.models import Avg
from rest_framework import viewsets
from rest_framework import filters, permissions
from rest_framework.pagination import LimitOffsetPagination

from yamdb.models import Categories, Genres, Comment, Review, Titles
from .mixins import CreateListDestroyViewSet
from .permissions import AdminOrReadOnly, GetPermissionsReview
from .serializer import (CommentSerializer, ReviewSerializer,
                         CategoriesSerializer, GenresSerializer,
                         TitlesSerializer, ReadOnlyTitleSerializer)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all().annotate(Avg('reviews__score'))
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadOnlyTitleSerializer
        return TitlesSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [GetPermissionsReview, permissions.IsAdminUser]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
