from django.contrib import admin

from .models import User


@admin.register(User)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('user', 'email')
    empty_value_display = '-пусто-'
