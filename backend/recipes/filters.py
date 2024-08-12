from django_filters import rest_framework

from .models import Recipe, Tag
from recipes.models import Recipe


class RecipeFilter(rest_framework.FilterSet):
    """Фильтрация избранных для отображения.
    Фильтрация по тегам, множественное.
    Фильтрация списка покупок.
    """
    is_favorited = rest_framework.BooleanFilter(method='filter_is_favorited',)
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='filter_is_in_shopping_cart',
    )

    def filter_is_favorited(self, queryset, _, value):
        if hasattr(self.request, 'user'):
            user = self.request.user
            if user.is_authenticated and value:
                return queryset.filter(favorite_recipe__user=user)
        return queryset.all()

    def filter_is_in_shopping_cart(self, queryset, _, value):
        if hasattr(self.request, 'user'):
            user = self.request.user
            if user.is_authenticated and value:
                return queryset.filter(shopping_cart__user=user)
        return queryset.all()

    class Meta:
        model = Recipe
        fields = ('author',
                  'tags',
                  'is_favorited',
                  'is_in_shopping_cart',
                  )