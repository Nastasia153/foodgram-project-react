from django.db import IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from recipes.models import User, Tag, Ingredient, Recipe
from .permissions import IsAdminAsDefinedByUserModel
from .serializers import (
    UserSerializer, SignUpSerializer, TokenRequestSerializer,
    CurrentUserSerializer, TagSerializer, IngredientSerializer,
    RecipeSerializer
)
from .services import confirmation_email, generate_confirmation_code
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
)
from rest_framework.decorators import action, api_view, permission_classes
from .mixins import AuthorOnlyMixin


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all().order_by('ingr_name')
    serializer_class = IngredientSerializer
    lookup_field = 'ingr_name'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('ingr_name',)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(AuthorOnlyMixin, viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsAdminAsDefinedByUserModel,)
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


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регистрация пользователя и отправка кода подтверждения"""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(
            defaults={'is_active': False},
            **serializer.validated_data
        )
    except IntegrityError:
        return HttpResponseBadRequest(
            'Пользователь с таким именем или адресом уже существует'
        )
    user.code = generate_confirmation_code()
    user.save()
    confirmation_email(user.email, user.code)
    return Response({"email": user.email, "username": user.username})


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Проверка кода подтверждения"""
    serializer = TokenRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    confirmation_code = serializer.validated_data['confirmation_code']
    if confirmation_code != user.code:
        return HttpResponseBadRequest('Неверный код подтверждения')
    user.is_active = True
    user.save()
    return Response({'token': str(RefreshToken.for_user(user).access_token)})

