from django.urls import include, path
from rest_framework import routers

from .views import (
    TagViewSet, IngredientViewSet, RecipeViewSet,
    FavoriteViewSet, SubscribeViewSet, UserViewSet, signup, token
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register(r'users/(?P<users_id>\d+)/subscribe',
                SubscribeViewSet, basename='subscribe')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register(r'recipes/(?P<pecipes_id>\d+)/favorite',
                FavoriteViewSet, basename='favorite')

auths = [
    path('signup/', signup),
    path('token/', token)
]

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include(auths))
]