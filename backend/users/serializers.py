from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import Recipe
from .mixins import ValidateUsernameMixin
from .models import User, Follow
from .validators import username_validator
from djoser.serializers import UserSerializer as DjoserUserSerializer


class UserSerializer(ValidateUsernameMixin, serializers.Serializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class CurrentUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        pass


class SignUpSerializer(ValidateUsernameMixin, serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150, validators=(username_validator(),)
    )


class TokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField()


class SubscribeSerializer(serializers.Serializer):
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
        request_user = self.context.get('request').user.id
        queryset = Follow.objects.filter(author=obj.author,
                                         follower=request_user).exists()
        return queryset

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author).all()
        return queryset

    def get_recipe_count(self, obj):
        return obj.author.recipes.count


# class SubscriptionsSerializer(DjoserUserSerializer):
#     class Meta:
#         model = Follow
#         fields = ('user', 'author')
#
#     def performe_create(self):
#         pass

