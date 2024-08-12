from django.core.validators import MinLengthValidator
from django.db import models

from backend.variables import (MAX_NUM_20,
                               MAX_NUM_254, MIN_NUM_2)


class Ingredient(models.Model):
    """Модель ингредиентов, поля имени и еденицы измерения.
    Для заполнения БД используй скрипт в папке data.
    """
    name = models.CharField(
        max_length=MAX_NUM_254,
        verbose_name='Ингредиент',
        default='Нет ингредиента',
        validators=[
            MinLengthValidator(
                MIN_NUM_2,
                'Имя ингредиента должно быть больше 2 символов.')
        ],)
    measurement_unit = models.CharField(
        max_length=MAX_NUM_20,)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self) -> str:
        return (f'Ингредиент: {self.name} '
                f'единица измерения: {self.measurement_unit}')
