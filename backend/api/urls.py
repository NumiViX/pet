from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from ingredients.views import IngredientViewSet
from recipes.views import RecipeViewSet
from tags.views import TagViewSet
from rest_framework.authtoken import views


router_v1 = DefaultRouter()

router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientViewSet)
router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router_v1.urls)),
    #path('api-token-auth/', views.obtain_auth_token),
    #re_path(r'^auth/', include('djoser.urls.jwt')),
    #re_path(r'^auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
