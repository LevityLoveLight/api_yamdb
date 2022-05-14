from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg
from reviews.models import Review, Comment, Categories, Genres, Title
from rest_framework import serializers
from users.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator


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
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'genre', 'description')


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'text',
            'author',
            'score',
            'pub_date'
        ]
        extra_kwargs = {'title': {'required': False}}

    def validate(self, data):
        title = self.context.get('title')
        request = self.context.get('request')
        if (
            request.method != 'PATCH' and
            Review.objects.filter(title=title, author=request.user).exists()
        ):
            raise serializers.ValidationError('Score already exists')
        return data


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
