from yamdb.models import Review, Comment, Categories, Genres, Titles
from rest_framework import serializers
from users.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True
    )
    description = serializers.CharField(required=False)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'category', 'genre', 'description')


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True),
    year = serializers.DateField(read_only=True),
    category = CategoriesSerializer(read_only=True),
    genre = GenresSerializer(read_only=True),
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Titles
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'category',
            'genre',
            'description',
        )


class ReviewSerializer(serializers.ModelSerializer):
    model = Review

    class Meta:
        fields = [

        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = [
            'id',
            'text',
            'author',
            'pub_date',
        ]
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                                'bio', 'email', 'role']


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {'Выберите другой username'})
        return data


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user,
            data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data
