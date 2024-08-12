from colorfield.fields import ColorField
from django.core.validators import MinLengthValidator
from django.db import models

from backend.variables import (COLOR_CHOICES, MAX_NUM_20, MIN_NUM_3)


class Tag(models.Model):
    """Модель тегов, с возможностью выбора цвета тега."""
    name = models.CharField(
        max_length=MAX_NUM_20,
        verbose_name='Тег',
        validators=[
            MinLengthValidator(MIN_NUM_3, 'Тег должен быть больше 3 символов.')
        ],)
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
        max_length=MAX_NUM_20,
        validators=[
            MinLengthValidator(
                MIN_NUM_3,
                'slug должен быть больше 3 символов.')
        ],)
    color = ColorField(
        choices=COLOR_CHOICES,
        default='#FF0000',)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name