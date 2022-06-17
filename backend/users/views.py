from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet

from .validators import username_validator
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
