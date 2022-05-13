from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'


class User(AbstractUser):

    ROLE = (
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField('e-mail', unique=True)
    username = models.CharField("Имя пользователя", max_length=50,
                                blank=True, null=True, unique=True)
    role = models.CharField("Роль пользователя", max_length=10,
                            choices=ROLE, default=USER)

    @property
    def is_admin(self):
        return any(
            [self.role == ADMIN, self.is_superuser, self.is_staff]
        )

    @property
    def is_moderator(self):
        return self.ROLE == MODERATOR

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id']
