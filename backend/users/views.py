from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import CustomPagination
from api.permissions import IsOwnerAdmin
from .models import Follow
from .serializers import SubscribeSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для работы с пользователем."""
    queryset = User.objects.all()
    pagination_class = CustomPagination

    @action(methods=['post', 'delete'], detail=True,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id=None):
        """Эндпоинт подписки/отписки."""
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            is_exist = Follow.objects.filter(
                user_id=request.user.id, author_id=author.id).exists()
            if is_exist or request.user == author:
                return Response({
                    'detail': 'Подписка есть или пытайтесь подписаться на себя'
                }, status=status.HTTP_400_BAD_REQUEST)
            new_sub = Follow.objects.create(user=request.user, author=author)
            serializer = SubscribeSerializer(new_sub,
                                             context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(
                Follow, user=request.user, author=author
            )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise MethodNotAllowed(request.method)

    @action(methods=['get'], detail=False,
            serializer_class=SubscribeSerializer,
            permission_classes=(IsOwnerAdmin,))
    def subscriptions(self, request):
        """Эндпоинт всех подписок пользователя."""
        queryset = Follow.objects.filter(user_id=request.user.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)
