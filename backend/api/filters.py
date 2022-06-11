import django_filters

from recipes.models import Recipe


class RacipeFilter(django_filters.FilterSet):
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filters.BooleanFilter(
        method='filter_is_favorited'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

#
# class TitleFilter(django_filters.FilterSet):
#     """Фильтр по названию, году выхода, жанру и категории"""
#     name = django_filters.CharFilter(field_name='name',
#                                      lookup_expr='icontains')
#     year = django_filters.NumberFilter(field_name='year')
#     genre = django_filters.CharFilter(field_name='genre__slug')
#     category = django_filters.CharFilter(field_name='category__slug')
#
#     class Meta:
#         model = Title
#         fields = ('name', 'year', 'genre', 'category')
