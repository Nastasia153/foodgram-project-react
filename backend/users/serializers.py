import api.serializers
from django.contrib.auth import get_user_model
from djoser.serializers import (UserSerializer as DjoserUserSerializer,
                                UserCreateSerializer as DjoserCreateSerializer,
                                SetPasswordSerializer)
from recipes.models import Recipe
from rest_framework import serializers

from .mixins import ValidateUsernameMixin
from .models import FoodgramUser, Follow

User = get_user_model()


class IsSubscribed(metaclass=serializers.SerializerMetaclass):
    """Мета клас для проверки подписки пользователя на автора."""
    is_subscribed = serializers.SerializerMethodField()

    def __init__(self):
        self.context = None

    def get_is_subscribed(self, obj):
        """Проверка подписки пользователя."""
        request = self.context.get('request')
        if Follow.objects.filter(user=request.user, author_id=obj.id).exists():
            return True
        return False


class UserSerializer(DjoserUserSerializer, IsSubscribed):
    """Сериализатор модели User."""
    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = (DjoserUserSerializer.Meta.fields
                  + ('is_subscribed',))

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data.pop('password', None)
        return data


class UserCreateSerializer(DjoserCreateSerializer,
                           ValidateUsernameMixin,
                           IsSubscribed):
    """Сериализатор создания нового пользователя."""
    class Meta(DjoserCreateSerializer.Meta):
        fields = (DjoserCreateSerializer.Meta.fields
                  + ('is_subscribed',))


class SubscribeSerializer(serializers.ModelSerializer, IsSubscribed):
    """Сериализатор подписки/отписки."""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    # def get_is_subscribed(self, obj):
    #     print(f'type obj: {obj}')
    #     request = self.context.get('request')
    #     return request.user.is_authenticated and Follow.objects.filter(
    #         user=request.user, author__id=obj.id).exists()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author).all()
        return api.serializers.MiniViewRecipeSerializer(queryset,
                                                        many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class UserSetPasswordSerializer(SetPasswordSerializer):
    class Meta:
        model = FoodgramUser
        fields = ('new_password', 'current_password')
