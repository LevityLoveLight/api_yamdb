from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.CharField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Titles(models.Model):
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
    )
    name = models.CharField(
        'Название',
        max_length=256
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    year = models.DateField(
        'Дата добавления'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
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
