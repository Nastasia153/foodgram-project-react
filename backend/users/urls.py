from django.urls import include, path
from rest_framework import routers

from . import views
from .views import token

app_name = 'users'

router = routers.DefaultRouter()

router.register('users', views.UserViewSet, basename='user')
router.register(r'users/(?P<users_id>\d+)/subscribe',
                views.SubscribeViewSet, basename='subscribe')

# auths = [
#     path('token/login/', token),
#     # path('token/logout', )
# ]

urlpatterns = [
    path('api/', include(router.urls)),
    # path('api/auth/', include(auths))
]
