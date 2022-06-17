from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'ingredients', views.IngredientViewSet, basename='ingredient')
router.register(r'recipes', views.RecipeViewSet, basename='recipe')
router.register(r'recipes/(?P<pecipes_id>\d+)/favorite',
                views.FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('api/', include(router.urls))
]
