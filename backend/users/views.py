from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.permissions import IsAdminOrAuthorOrReadOnly, IsOwnerAdmin

from .models import Follow
from .serializers import SubscribeSerializer, UserSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """Вьюсет для работы с пользователем."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrAuthorOrReadOnly,)

    @action(methods=['GET'], detail=False,
            permission_classes=(IsOwnerAdmin,))
    def me(self, request, *args, **kwargs):
        """Эндпоинт профиля пользователя."""
        if request.method == "GET":
            serializer = UserSerializer(
                self.request.user, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise MethodNotAllowed(request.method)

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            is_exist = Follow.objects.filter(
                user=request.user, author=author).exists()
            if is_exist or request.user == author:
                return Response({
                    'error': 'Подписка есть или пытайтесь подписаться на себя'
                }, status=status.HTTP_400_BAD_REQUEST)
            new_sub = Follow.objects.create(user=request.user, author=author)
            serializer = SubscribeSerializer(
                new_sub, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(
                Follow, user=request.user, author=author
            )
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise MethodNotAllowed(request.method)

    # error: AttributeError at /api/users/subscriptions/
    # Got AttributeError when attempting to get a value for field `email` on serializer `UserSerializer`.
    # The serializer field might be named incorrectly and not match any attribute or key on the `Follow` instance.
    # Original exception text was: 'Follow' object has no attribute 'email'.
    #
    # @action(methods=['GET'], detail=False,
    #         permission_classes=(IsAuthenticated,))
    # def subscriptions(self, request):
    #     """Эндпоинт всех подписок пользователя."""
    #     page = self.paginate_queryset(self.request.user.follower.all())
    #     serializer = UserSerializer(page, many=True,
    #                                 context={'request': request,
    #                                          'action': True})
    #     return self.get_paginated_response(
    #         serializer.to_representation(serializer.instance))
