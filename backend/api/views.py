from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag, RecipeIngredients

from .filters import RecipeFilter, IngredientFilter
from .permissions import (IsAdminOrAuthorOrReadOnly, IsAdminUserOrReadOnly,
                          IsOwnerAdmin)
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          TagSerializer, ShoppingCartSerializer, MiniViewRecipeSerializer)
from .pagination import CustomPagination


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """Вьюсет для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = IngredientFilter
    pagination_class = None
    permission_classes = (IsAdminUserOrReadOnly,)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """Вьюсет для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminUserOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецепта."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeReadSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminOrAuthorOrReadOnly)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        """Сохранение пользователя как автора рецепта."""
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Выбор сериализатора под запрос."""
        if self.action in ['create', 'partial_update']:
            return RecipeWriteSerializer
        return RecipeReadSerializer

    @action(methods=['post', 'delete'], detail=True,
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
            old_fav = get_object_or_404(Favorite,
                                        user=request.user,
                                        recipe=recipe)
            self.perform_destroy(old_fav)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise MethodNotAllowed(request.method)

    @action(methods=['POST', 'DELETE'], detail=True,
            permission_classes=(IsOwnerAdmin,))
    def shopping_cart(self, request, pk):
        """Корзина."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                return Response({'detail': 'Рецепт уже в корзине.'},
                                status=status.HTTP_400_BAD_REQUEST)
            add_recipe = ShoppingCart.objects.create(user=request.user,
                                                     recipe=recipe)
            serializer = ShoppingCartSerializer(add_recipe,
                                            context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            instance = get_object_or_404(
                ShoppingCart, user=request.user, recipe=recipe)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise MethodNotAllowed(request.method)

    # "detail": "Невозможно удовлетворить \"Accept\" заголовок запроса." 406
    @action(detail=False, methods=['get'],
            permission_classes=(IsOwnerAdmin,))
    def download_shopping_cart(self, request):
        """"Вывод списка покупок в текстовый файл."""
        cart = RecipeIngredients.objects.filter(recipe__shopping_cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').order_by('ingredient__name').annotate(total=Sum('amount'))
        # shopping_list = ShoppingCart.objects.filter(recipe__shopping_cart__user=request.user).values(
        #     'recipe__ingredients__name', 'recipe__ingredients__measurement_unit').order_by(
        #     'recipe__ingredients__name').annotate(ingredients_total=Sum('recipe__ingredient_recipe__amount'))
        print(cart)
        # ingredients_list = RecipeIngredients.objects.filter(recipe_id__in=shopping_list).order_by('ingredient')
        # print(ingredients_list)
        text = cart
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="shopping_list.txt"'
        return response
