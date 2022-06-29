from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

from .validators import username_validator


class FoodgramUser(AbstractUser):
    """Модель пользователя."""
    USER = 'user'
    ADMIN = 'admin'
    ROLES = ((USER, 'пользователь'),
             (ADMIN, 'админ'))

    username = models.CharField(
        'имя пользователя', max_length=150, unique=True,
        validators=(username_validator(),)
    )
    email = models.EmailField('электронная почта', max_length=254, unique=True)
    first_name = models.CharField('имя', max_length=150, null=True)
    last_name = models.CharField('фамилия', max_length=150, null=True)
    role = models.CharField('роль',
                            max_length=max(len(key) for key, _ in ROLES),
                            choices=ROLES, default=USER)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('date_joined',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (self.is_staff
                or self.role == FoodgramUser.ADMIN
        )


User = get_user_model()


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор рецепта'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follower'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='check_following'
            )
        ]
        verbose_name = 'подписки'
        verbose_name_plural = 'подписки'
        ordering = ('id',)
