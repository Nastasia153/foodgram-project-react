from django.urls import include, path
from rest_framework import routers

from users import views as user_views
from . import views

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', user_views.UserViewSet, basename='user')
router.register('tags', views.TagViewSet, basename='tag')
router.register('ingredients', views.IngredientViewSet, basename='ingredient')
router.register('recipes', views.RecipeViewSet, basename='recipe')
router.register(r'recipes/(?P<pecipes_id>\d+)/favorite',
                views.FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('api/', include(router.urls)),
    # path('api/auth/', include('djoser.urls'))
]
