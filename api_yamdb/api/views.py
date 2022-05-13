from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


from rest_framework import viewsets, status
from rest_framework import filters, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes, action, api_view



from yamdb.models import Categories, Genres, Comment, Review, Titles, User
from .mixins import CreateListDestroyViewSet
from .permissions import AdminOrReadOnly, ReviewPermissions, IsAdmin
from .serializer import (CommentSerializer, ReviewSerializer,
                         CategoriesSerializer, GenresSerializer,
                         TitlesSerializer, ReadOnlyTitleSerializer,
                         UserSerializer, UserCreateSerializer,
                         UserTokenSerializer)


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
    permission_classes = (ReviewPermissions,)
    pagination_class = LimitOffsetPagination


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ReviewPermissions,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id')
        post = get_object_or_404(Comment, pk=comment_id )
        return post.comments.filter(post_id=comment_id )

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user.username)
        serializer.save(author=user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(self.request.user,
                                    data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = UserTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    default_token_generator.check_token(user, confirmation_code)
    refresh = RefreshToken.for_user(user)
    return Response({
        'token': (refresh.access_token)},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        user, _ = User.objects.get_or_create(username=username, email=email)
    except Exception:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        "Yambd account activation",
        "confirmation_code: " + confirmation_code,
        "admin@yambd.com",
        [email],
        fail_silently=False,
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )