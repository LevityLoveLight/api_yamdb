from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLE = 'user'
ADMIN_ROLE = 'admin'
MODERATOR_ROLE = 'moderator'


class User(AbstractUser):

    ROLE = (
        (USER_ROLE, 'user'),
        (ADMIN_ROLE, 'admin'),
        (MODERATOR_ROLE, 'moderator'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField('e-mail', unique=True)
    username = models.CharField("Имя пользователя", max_length=50,
                                blank=True, null=True, unique=True)
    role = models.CharField("Роль пользователя", max_length=10,
                            choices=ROLE, default=USER_ROLE)

    class Meta:
        ordering = ("username",)
