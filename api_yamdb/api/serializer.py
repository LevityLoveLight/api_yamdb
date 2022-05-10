from yamdb.models import Review, Comment, Categories, Genres, Titles
from rest_framework import serializers


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'


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
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True),
    year = serializers.DateField(read_only=True),
    category = CategoriesSerializer(read_only=True),
    genre = GenresSerializer(read_only=True),
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Titles
        fields = '__all__'


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

