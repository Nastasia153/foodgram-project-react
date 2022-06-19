from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'users'

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls')),
    path(r'api/auth/', include('djoser.urls.authtoken'))
]
