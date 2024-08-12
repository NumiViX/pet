from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag
from backend.variables import (MAX_NUM_50, MAX_NUM_254, MAX_NUM_500,
                               MAX_NUM_5000, MIN_NUM_1, MIN_NUM_2)


User = get_user_model()


class Recipe(models.Model):
    """Модель рецептов. Связан с моделью ингредиентов через
    промежуточную модель RecipeIngredient, где задано
    дополнительное поле amount.
    """
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',)
    image = models.ImageField(
        upload_to='api/images/',
        null=True,
        default=None,
        height_field=None,
        width_field=None,
        max_length=None,)
    name = models.CharField(
        max_length=MAX_NUM_254,
    )
    text = models.TextField(
        max_length=MAX_NUM_5000,
        validators=[
            MinLengthValidator(
                MAX_NUM_50,
                'Текст рецепта должен быть больше 50 символов.')
        ],)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MaxValueValidator(
                MAX_NUM_500,
                'Значение должно быть меньше 500.'),
            MinValueValidator(
                MIN_NUM_2,
                'Значение должно быть больше 2.'
            ),
        ],)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингридиенты',
        related_name='recipes',
        blank=True,)
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE,)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,)
    pub_update = models.DateTimeField(
        auto_now=True,)
    is_published = models.BooleanField(
        default=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return f'Название рецепта: {self.name}'


class RecipeIngredient(models.Model):
    amount = models.PositiveSmallIntegerField(
        verbose_name='количество',
        validators=[
            MaxValueValidator(
                MAX_NUM_5000,
                'Количество ингредиента больше 5000'),
            MinValueValidator(
                MIN_NUM_1,
                'Количество ингредиента меньше 1-го'),
        ],
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredient',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredient',
    )

    class Meta:
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        ordering = ('recipe',)

    def __str__(self) -> str:
        return (f'В рецепте {self.recipe.name} присутствует ингредиент: '
                f'{self.ingredients.name} в количестве '
                f'{self.amount} {self.ingredients.measurement_unit}')


class Favorite(models.Model):
    """Модель для реализации возможности добавления в избранное."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('recipe',)

    def __str__(self) -> str:
        return f'{self.recipe.name} в избранном у {self.user.get_username}'


class ShoppingCart(models.Model):
    """Реализует возможность добавлять рецепты в список покупок.
    Далее, появляется возможность распечатать ингредиенты и их количчество."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Лист покупок'
        verbose_name_plural = 'Лист покупок'
        ordering = ('user',)

    def __str__(self) -> str:
        return (f'{self.recipe.name} в списке '
                f'покупок у {self.user.get_username()}')
