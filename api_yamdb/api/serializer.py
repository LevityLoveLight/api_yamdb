from yamdb.models import Review, Comment
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    model = Review

    class Meta:
        fields = [

        ]


class CommentSerializer(serializers.ModelSerializer):
    model = Comment

    class Meta:
        fields = [

        ]