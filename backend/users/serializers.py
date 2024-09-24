from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.serializers import RecipeViewSerializer
from .models import Subscribe

User = get_user_model()


class RegistrationSerializer(UserCreateSerializer):
    """Добавление полей при регистрации."""
    email = serializers.EmailField(required=True)

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class IsSubscribedMixin:
    """Миксин для проверки подписки пользователя на автора."""
    def get_is_subscribed(self, obj: User) -> bool:
        request = self.context.get('request')
        if request.user.is_anonymous or request.user == obj:
            return False
        return obj.subscribed.filter(user=request.user).exists()


class UserSerializer(
    #IsSubscribedMixin, 
    UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    email = serializers.EmailField()

    class Meta(UserSerializer):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        return getattr(obj, 'is_subscribed', False)


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = (
            'author',
            'user',
        )

    def validate(self, data: dict) -> dict:
        author = data.get('author')
        user = data.get('user')
        if user == author:
            raise serializers.ValidationError('Вы не можете подписаться на самого себя.')
        if author.subscribed.filter(user=user).exists():
            raise serializers.ValidationError('Вы уже подписаны.')
        return data


class SubscribeRepresentSerializer(IsSubscribedMixin, serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj: User) -> int:
        return obj.recipes.count()

    def get_recipes(self, obj: User) -> list:
        request = self.context.get('request')
        context = {'request': request}
        queryset = obj.recipes.all()

        recipe_limit = self.get_recipe_limit(request)
        if recipe_limit is not None:
            queryset = queryset[:recipe_limit]

        return RecipeViewSerializer(queryset, context=context, many=True).data

    @staticmethod
    def get_recipe_limit(request) -> int:
        """Обработка параметра recipe_limit из запроса."""
        try:
            return int(request.query_params.get('recipe_limit'))
        except (TypeError, ValueError):
            return None
