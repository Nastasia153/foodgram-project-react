from django_filters import FilterSet, ModelMultipleChoiceFilter, NumberFilter
from django_filters import rest_framework as filters

from recipes.models import Recipe, Tag


class IngredientFilter(filters.FilterSet):
    """Фильтр ингредиента по началу слова."""
    name = filters.CharFilter(lookup_expr='istartswith')


class RecipeFilter(FilterSet):
    """Фильтр для выдачи рецептов"""
    is_favorited = NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = NumberFilter(method='filter_is_in_cart')
    tags = ModelMultipleChoiceFilter(field_name='tags__slug',
                                     to_field_name='slug',
                                     queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart',)

    def filter_is_favorited(self, queryset, name, value):
        """Фильтр по избранному."""
        if self.request.user.is_authenticated:
            if int(value) == 1:
                return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_is_in_cart(self, queryset, name, value):
        """Фильтр по добавленному в корзину."""
        if self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
