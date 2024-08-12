from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import (Favorite, Recipe, RecipeIngredient, ShoppingCart)
from .pagination import NewPagination
from .pdf_file_creating import create_pdf_file
from .serializers import (FavoriteSerializer, RecipeSerializer,
                          RecipeViewSerializer, ShoppingCartSerializer)


User = get_user_model()
    

class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для рецептов с функционалом избранного и корзины покупок."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Recipe.objects.all()
    pagination_class = NewPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeViewSerializer
        return RecipeSerializer

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        return self._handle_favorite_or_cart(request, pk, FavoriteSerializer, 'favorite_recipe')

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self._handle_favorite_or_cart(request, pk, ShoppingCartSerializer, 'shopping_cart')

    def _handle_favorite_or_cart(self, request, pk, serializer_class, related_name):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        if request.method == 'POST':
            serializer = serializer_class(data={'user': user.id, 'recipe': recipe.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        related_manager = getattr(recipe, related_name)
        if not related_manager.filter(user=user).exists():
            return Response({"detail": "Not found in user's list."}, status=status.HTTP_400_BAD_REQUEST)
        
        subscription = related_manager.get(user=user)
        self.perform_destroy(subscription)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_cart_data = self._get_shopping_cart_data(request.user)
        buffer = create_pdf_file(shopping_cart_data)
        return self._generate_pdf_response(buffer)

    def _get_shopping_cart_data(self, user):
        return RecipeIngredient.objects.filter(
            recipeshopping_cartuser=user
        ).values('ingredientsname', 'ingredientsmeasurement_unit').annotate(amount=Sum('amount'))

    def _generate_pdf_response(self, buffer):
        now = datetime.now()
        timestamp = now.strftime('%Y_%m_%d')
        filename = f'ingredients_{timestamp}.txt'
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
