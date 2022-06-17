from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from recipes.models import User, Tag, Ingredient, Recipe
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (
    TagSerializer, IngredientSerializer,
    RecipeWriteSerializer, RecipeListSerializer
)
from rest_framework.pagination import PageNumberPagination


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all().order_by('id')
    serializer_class = IngredientSerializer
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-pub_date')
    serializer_class = RecipeWriteSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAdminOrAuthorOrReadOnly
    )
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return RecipeWriteSerializer
        return RecipeListSerializer


class FavoriteViewSet(viewsets.ModelViewSet):

    pass
