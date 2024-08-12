from rest_framework import serializers


from .models import Ingredient
from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )

    def to_internal_value(self, instance):
        return instance.id
