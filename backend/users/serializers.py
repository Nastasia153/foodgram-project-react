from django.contrib.auth import get_user_model
from djoser.serializers import SetPasswordSerializer
from djoser.serializers import UserCreateSerializer as DjoserCreateSerializer
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers

from recipes.models import Recipe
from .mixins import ValidateUsernameMixin
from .models import Follow, FoodgramUser

User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    """Сериализатор модели User."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = (DjoserUserSerializer.Meta.fields
                  + ('is_subscribed',))

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follow.objects.filter(user=user, author_id=obj.id).exists()
        return False

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data.pop('password', None)
        return data


class UserCreateSerializer(DjoserCreateSerializer,
                           ValidateUsernameMixin):
    """Сериализатор создания нового пользователя."""
    class Meta(DjoserCreateSerializer.Meta):
        fields = DjoserCreateSerializer.Meta.fields


class MiniViewRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
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

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follow.objects.filter(user=user, author_id=obj.id).exists()
        return False

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author).all()[:3]
        return MiniViewRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class UserSetPasswordSerializer(SetPasswordSerializer):
    class Meta:
        model = FoodgramUser
        fields = ('new_password', 'current_password')
