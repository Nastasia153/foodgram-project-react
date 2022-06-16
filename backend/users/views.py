from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from djoser.views import UserViewSet as DjoserUserViewSet
from .serializers import UserSerializer, CurrentUserSerializer, SubscribeSerializer, SubscriptionsSerializer
from .models import Follow

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_object(self):
        if self.action == 'me':
            return self.request.user
        return super().get_object()

    @action(
        methods=['GET', 'PATCH'], detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=CurrentUserSerializer
    )
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        raise MethodNotAllowed(request.method)


# class UserViewSet(DjoserUserViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     lookup_field = 'username'
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('username',)
#
#     def get_object(self):
#         if self.action == 'me':
#             return self.request.user
#         return super().get_object()
#
#     @action(
#         methods=['GET', 'PATCH'], detail=False,
#         permission_classes=(IsAuthenticated,),
#         serializer_class=CurrentUserSerializer
#     )
#     def me(self, request, *args, **kwargs):
#         if request.method == "GET":
#             return self.retrieve(request, *args, **kwargs)
#         elif request.method == "PATCH":
#             return self.partial_update(request, *args, **kwargs)
#         raise MethodNotAllowed(request.method)
#
#     @action(methods=['GET'], detail=False,
#             permission_classes=(IsAuthenticated,),
#             serializer_class=SubscriptionsSerializer)
#     def subscriptions(self, request):
#         pass
#
#     @action(detail=True,
#             methods=['POST', 'DELETE'],
#             permission_classes=(IsAuthenticated,)
#             )
#     def subscribe(self, request, id=None):
#         author = get_object_or_404(User, id=id)
#         if request.method == 'POST':
#             is_exist = Follow.objects.filter(
#                 user=request.user, author=author).exists()
#             if is_exist or request.user == author:
#                 return Response({
#                     'error': 'Подписка есть. Пытайтесь подписаться на себя?'
#                 }, status=status.HTTP_400_BAD_REQUEST)
#             new_sub = Follow.objects.create(user=request.user, author=author)
#             serializer = SubscribeSerializer(
#                 new_sub, context={'request': request}
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         if request.method == 'DELETE':
#             instance = get_object_or_404(
#                 Follow, user=request.user, author=author
#             )
#             self.perform_destroy(instance)
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         raise MethodNotAllowed(request.method)

    # @action(methods=['POST'], detail=False,
    #         permission_classes=IsAuthenticated)
    # def set_password(self, request, *args, **kwargs):
    #     pass




#     @action(methods=['POST'], detail=False,
#             permission_classes=(AllowAny,),
#             serializer_class=SignUpSerializer)
#     def signup(self, request):
#         serializer = SignUpSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             user, _ = User.objects.get_or_create(
#                 defaults={'is_active':False},
#                 **serializer.validated_data
#             )
#         except IntegrityError:
#             return HttpResponseBadRequest(
#                 'Пользователем с таким именем или адресом уже существует'
#             )
#         user.save()
#         return Response({"email":user.email, "username": user.username})
# 
# 
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def token(request):
#     """Проверка кода подтверждения"""
#     serializer = TokenRequestSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = get_object_or_404(
#         User, username=serializer.validated_data['username']
#     )
#     user.is_active = True
#     user.save()
#     return Response({'token': str(RefreshToken.for_user(user).access_token)})

