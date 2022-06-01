from django.urls import include, path
from rest_framework import routers

from .views import (
    TagViewSet, IngredientViewSet, RecipeViewSet,
    UserViewSet, signup, token
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')

auths = [
    path('signup/', signup),
    path('token/', token)
]

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include(auths))
]