from yamdb.models import Review, Comment
from rest_framework import serializers


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
