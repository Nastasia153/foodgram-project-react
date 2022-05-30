# import django_filters
#
# from recipes.models import Favorite
#
#
# class RacipeFilter(django_filters.FilterSet):
#     is_in_shopping_cart = django_filters.BooleanFilter(method='filter_is_in_shopping_cart')
#
#
# class
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
