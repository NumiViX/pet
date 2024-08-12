from django.contrib import admin

from recipes.models import Recipe
from backend.variables import MIN_NUM_1

from .models import Recipe, RecipeIngredient
from users.models import Subscribe


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)
    search_fields = ('user', 'author',)
    empty_value_display = '-пусто-'


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = MIN_NUM_1


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'recipe', 'ingredients',)
    search_fields = ('amount', 'recipe', 'ingredients',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('name', 'author',)
    search_fields = ('name', 'text',)
    list_filter = ('author', 'name', 'tags',)
    readonly_fields = ('is_favorited_count',)
    empty_value_display = '-пусто-'

    def is_favorited_count(self, obj):
        return obj.favorite_recipe.count()
