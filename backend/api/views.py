# from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag

from .permissions import (IsAdminOrAuthorOrReadOnly, IsAdminUserOrReadOnly,
                          IsOwnerAdmin)
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          TagSerializer)


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """Вьюсет для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    pagination_class = None
    permission_classes = IsAdminUserOrReadOnly


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """Вьюсет для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = IsAdminUserOrReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецепта."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeWriteSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAdminOrAuthorOrReadOnly
    )
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        """Сохранение пользователя как автора рецепта."""
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return RecipeWriteSerializer
        return RecipeReadSerializer

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=(IsOwnerAdmin,))
    def favorite(self, request, pk):
        """Избранное."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(user=request.user,
                                       recipe=recipe).exists():
                return Response({'detail': 'Рецепт уже добавлен в избранное.'},
                                status=status.HTTP_400_BAD_REQUEST)
            new_fav = Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = FavoriteSerializer(new_fav,
                                            context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(
                Favorite, user=request.user, recipe=recipe)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise MethodNotAllowed(request.method)

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=(IsOwnerAdmin,))
    def shopping_cart(self, request, pk):
        """Список покупок."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                return Response({'detail': 'Рецепт уже в корзине.'},
                                status=status.HTTP_400_BAD_REQUEST)
            add_recipe = ShoppingCart.objects.create(user=request.user,
                                                     recipe=recipe)
            serializer = FavoriteSerializer(add_recipe,
                                            context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(
                ShoppingCart, user=request.user, recipe=recipe)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise MethodNotAllowed(request.method)

    #  "detail": "Невозможно удовлетворить \"Accept\" заголовок запроса." 406
    # @action(methods=['GET'], detail=False,
    #         permission_classes=(IsOwnerAdmin,))
    # def download_shopping_cart(self, request):
    #     """Создание списка покупок для скачивания."""
    #     user = request.user
    #     # shopping_list = RecipeIngredients.objects.filter(user=request.user)
    #     shopping_cart_list = ShoppingCart.objects.filter(
    #         user_id=user.id).values_list('recipe', flat=True)
    #     ingredients_list = RecipeIngredients.objects.filter(
    #         recipe_id__in=shopping_cart_list).order_by('id')
    #     ingredients = {}
    #     for ingredient in ingredients_list:
    #         if ingredient in ingredients.keys():
    #             ingredients[ingredient.ingredient] += ingredient.amount
    #         else:
    #             ingredients[ingredient.ingredient] = ingredient.amount
    #     shopping_list = []
    #     for k, v in ingredients.items():
    #         shopping_list.append(f'{k.name} - {v} {k.dimension} \n')
    #
    #     response = HttpResponse(shopping_list, 'Content-Type: text/plain')
    #     response['Content-Disposition'] = (f'attachment;'
    #                                        'filename="Shopping-list.txt"')
    #     return response
