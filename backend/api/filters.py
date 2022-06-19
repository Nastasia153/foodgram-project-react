# import django_filters
# from recipes.models import Recipe, Favorite, ShoppingCart
#

# class RacipeFilter(django_filters.FilterSet):
#     is_in_shopping_cart = django_filters.BooleanFilter(
#         method='filter_is_in_shopping_cart'
#     )
#     tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
#     is_favorited = django_filters.BooleanFilter(
#         method='filter_is_favorited'
#     )
#
#     class Meta:
#         model = Recipe
#         exclude = ('image')
#
#     def filter_is_favorited(self, queryset, value):
#         """Фильтр по избранному."""
#         queryset = Favorite.objects.all()
#         if self.request.user.is_authenticated:
#             if int(value) == 1:
#                 return queryset.filter(**{'': self.request.user.})
#         return queryset
#
#     def filter_is_in_shopping_cart(self, queryset, value):
#         queryset = ShoppingCart.objects.all()
#         if self.request.user.is_authenticated:
#             if int(value) == 1:
#                 return queryset.filter(**{'': self.request.user})
#         return queryset
