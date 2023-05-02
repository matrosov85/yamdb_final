from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    email = models.EmailField(blank=False)
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        max_length=10, choices=ROLES, default='user'
    )
    conf_code = models.CharField(
        max_length=250
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]
        ordering = ('pk',)

    def __str__(self):
        return self.username
