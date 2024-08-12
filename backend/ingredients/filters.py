from django.db.models import Q
from django_filters import rest_framework

from .models import Ingredient


class IngredientsFilter(rest_framework.FilterSet):
    """Поиск ингредиента по полю name.
    Двойная фильтрация: по вхождению в начало названия,
    по вхождению в произвольное место.
    """
    name = rest_framework.CharFilter(
        method='filter_name',
    )

    def filter_name(self, queryset, _, value):
        return queryset.filter(Q(name__icontains=value) | Q(
            name__startswith=value)).distinct()

    class Meta:
        model = Ingredient
        fields = ('name',)
