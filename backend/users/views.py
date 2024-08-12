from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response


from .serializers import (SubscribeRepresentSerializer,
                          SubscribeSerializer)
from recipes.pagination import NewPagination


User = get_user_model()


class UserViewSet(UserViewSet):
    """Добавление новых поинтов в UserViewSet.
    /subscriptions для просмотра подписок.
    /subscribe для добавления и удаления автора в/из подписки."""
    pagination_class = NewPagination
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        queryset = self.paginate_queryset(
            User.objects.filter(subscribed__user=request.user)
        )
        serializer = SubscribeRepresentSerializer(
            queryset,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True, url_path='subscribe',
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            return self._create_subscription(request.user, author)
        return self._delete_subscription(request.user, author)

    def _create_subscription(self, user, author):
        if user.subscribed.filter(author=author).exists():
            return Response(
                {"detail": "Вы уже подписаны на этого автора."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SubscribeSerializer(data={
            'user': user.id,
            'author': author.id
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete_subscription(self, user, author):
        subscription = user.subscribed.filter(author=author).first()
        if not subscription:
            return Response(
                {"detail": "Подписка не найдена."},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
