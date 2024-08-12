import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.validators import (MaxLengthValidator, MaxValueValidator,
                                    MinLengthValidator, MinValueValidator,
                                    RegexValidator)
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.serializers import UserSerializer

from backend.variables import (MAX_NUM_50, MAX_NUM_500, MAX_NUM_5000,
                               MIN_NUM_1, MIN_NUM_2)
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from tags.serializers import TagSerializer

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64')
            ext = format.split('/')[-MIN_NUM_1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name='temp.' + ext,
            )
        return super().to_internal_value(data)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = (
            'recipe',
            'user',
        )

    def validate(self, data):
        recipe = data.get('recipe')
        user = data.get('user')
        if recipe.favorite_recipe.filter(user=user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны.'
            )
        return data

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = (
            'recipe',
            'user',
        )

    def validate(self, data):
        recipe = data.get('recipe')
        user = data.get('user')
        if recipe.shopping_cart.filter(user=user).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в список покупок.'
            )
        return data

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe
        ).data


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=[
            MinValueValidator(
                MIN_NUM_1,
                'Значаени должно быть больше 1-го'),
            MaxValueValidator(
                MAX_NUM_5000,
                'Значение должно быть меньше 5000')
        ]
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    text = serializers.CharField(validators=[
        MinLengthValidator(
            MAX_NUM_50,
            'Текст рецепта меньше 50 символов.'),
        MaxLengthValidator(
            MAX_NUM_5000,
            'Текст рецепта больше 5000 символов.'),
        RegexValidator(r'^[\w\s!.,:;-?()"\']*$', (
            'Тескт рецепта содержит недопустимые символы. '
            'Допустимы цифры, пробелы, '
            'и знаки препинания:":.,\"\'-?()!".')),
        UniqueValidator(
            queryset=Recipe.objects.all(),
            message='Данный рецепт уже был создан.'),
    ])
    tags = serializers.SlugRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        slug_field='id',
    )
    ingredients = RecipeIngredientSerializer(
        many=True,
    )
    image = Base64ImageField(
        max_length=None,
        required=True,
        allow_empty_file=False,
        use_url=True,
    )
    cooking_time = serializers.IntegerField(
        validators=[
            MinValueValidator(
                MIN_NUM_2,
                'Значаени должно быть больше 2'),
            MaxValueValidator(
                MAX_NUM_500,
                'Значение должно быть меньше 500')
        ]
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'name',
            'image',
            'text',
            'cooking_time',
            'ingredients',
        )

    def to_representation(self, recipe):
        return RecipeViewSerializer(
            recipe,
            context={'request': self.context.get('request')},
        ).data

    def create_update_ingredients(self, recipe, ingredients, func=None):
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_obj = Ingredient.objects.get(id=ingredient.get('id'))
            amount = ingredient.get('amount')
            ingredient_list.append(RecipeIngredient(
                recipe=recipe,
                ingredients=ingredient_obj,
                amount=amount,))
        if func is not None:
            func()
        RecipeIngredient.objects.bulk_create(ingredient_list)

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(
            author=author,
            **validated_data)
        recipe.tags.set(tags)
        self.create_update_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags',)
        instance.name = validated_data.pop(
            'name',
            instance.name)
        instance.image = validated_data.pop(
            'image',
            instance.image)
        instance.text = validated_data.pop(
            'text',
            instance.text)
        instance.cooking_time = validated_data.pop(
            'cooking_time',
            instance.cooking_time,)
        ingredients = validated_data.get(
            'ingredients', [])
        instance.tags.clear()
        instance.tags.set(tags)
        recipe = instance
        func = instance.ingredients.clear
        self.create_update_ingredients(recipe, ingredients, func)
        instance.save()
        return instance


class RecipeIngredientViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
            'name',
            'measurement_unit',
        )


class RecipeViewSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра рецептов, в том числе анонимного."""
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientViewSerializer(
        read_only=True,
        many=True,
        source='recipeingredient',)
    tags = TagSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(required=False,
                             allow_null=True,
                             read_only=True,)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite_recipe.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()