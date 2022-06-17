from django.contrib.auth import get_user_model

from .models import FoodgramUser as User
from .mixins import ValidateUsernameMixin
from djoser.serializers import UserSerializer as DjoserUserSerializer

# User = get_user_model()


class UserSerializer(ValidateUsernameMixin, DjoserUserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
