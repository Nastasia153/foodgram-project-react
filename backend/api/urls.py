from django.urls import include, path
from rest_framework import routers

from . import views
from users import views as user_views

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', views.TagViewSet, basename='tag')
router.register('ingredients', views.IngredientViewSet, basename='ingredient')
router.register('users', user_views.UserViewSet, basename='user' )
router.register('recipes', views.RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
