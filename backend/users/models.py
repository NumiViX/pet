from django.contrib.auth.models import AbstractUser
from django.db import models


from backend.variables import MAX_NUM_254


class User(AbstractUser):
    """Переопределение поля email теперь должно быть уникальным.
    Переопределение USERNAME_FIELD для возможности авторизации по email.
    Добавление обязательных полей при регистрации 'first_name', 'last_name'.
    """
    email = models.EmailField(max_length=MAX_NUM_254, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


class Subscribe(models.Model):
    """Модель подписчиков, для реализации возможности
    подписок и просмотра их рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed',
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        ordering = ('author',)

    def __str__(self) -> str:
        return (f'Пользователь {self.user.get_username()}'
                f' подписан на: {self.author.get_username()}')
