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
                    'detail': 'Подписка есть или пытайтесь подписаться на себя'
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

#     @action(methods=['GET'], detail=False,
#             permission_classes=(IsOwnerAdmin,))
#     def subscriptions(self, request):
#         """Эндпоинт всех подписок пользователя."""
#         user = self.request.user
#         serializer = SubscribeSerializer(
#             Follow.objects.filter(user_id=user.id), many=True)
#         print(serializer.data)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#         # user = self.request.user
#         #queryset = Follow
# AttributeError at /api/users/subscriptions/
# 'NoneType' object has no attribute 'user'
#   File "C:\dev\foodgram-project-react\backend\users\serializers.py", line 36, in get_is_subscribed
#     request_user = self.context.get('request').user.id
