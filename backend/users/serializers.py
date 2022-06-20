import api.serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as DjoserUserSerializer
from recipes.models import Recipe
from rest_framework import serializers

from .mixins import ValidateUsernameMixin
from .models import Follow

User = get_user_model()


class UserSerializer(ValidateUsernameMixin, DjoserUserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class SubscribeSerializer(serializers.ModelSerializer):
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
        # print('Type of obj:', type(obj))
        request_user = self.context.get('request').user.id
        queryset = Follow.objects.filter(author=obj.author,
                                         user=request_user).exists()
        return queryset

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author).all()
        return api.serializers.RecipeReadSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')

    def create(self, validated_data):
        return User.objects.create(**validated_data)
