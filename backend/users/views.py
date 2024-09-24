from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from djoser.views import UserViewSet
from djoser.conf import settings
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Exists, OuterRef, Subquery

from backend.users.services.subscription_service import SubscriptionService

from .serializers import (SubscribeRepresentSerializer,
                          SubscribeSerializer, UserSerializer)
from recipes.pagination import NewPagination
from .models import Subscribe


User = get_user_model()


class UserViewSet(UserViewSet):
    """Добавление новых поинтов в UserViewSet.
    /subscriptions для просмотра подписок.
    /subscribe для добавления автора в подписки и удаления из подписок."""
    pagination_class = NewPagination
    permission_classes = [permissions.IsAuthenticated,]

    def get_serializer_class(self):
        if self.action == 'subscriptions':
            return settings.SERIALIZERS.subscriptions_confirm
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.action == 'subscriptions':
            self.permission_classes = settings.PERMISSIONS.subscriptions
        if self.action == 'subscriptions':
            self.permission_classes = settings.PERMISSIONS.subscribe
        return super().get_permissions()

    @action(detail=False,)
    def subscriptions(self, request):
        queryset = self.paginate_queryset(
            User.objects.filter(subscribed__user=request.user)
        )
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            queryset,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True, url_path='subscribe',)
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        service = SubscriptionService(request.user)
        if request.method == 'POST':
            return service._create_subscription(request.user, author)
        return service._delete_subscription(request.user, author)

