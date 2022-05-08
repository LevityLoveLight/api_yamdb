from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор ревью'
    )
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор ревью'
    )
    pub_date = models.DateTimeField(auto_now=True)
