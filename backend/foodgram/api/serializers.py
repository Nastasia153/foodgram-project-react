from rest_framework import serializers
from recipes.models import Tag, Ingredient, User, Recipe
from recipes.validators import username_validator
from .mixins import ValidateUsernameMixin


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('tag_name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'ingr_name', 'measurement_unit')
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.CharField

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'author', 'pub_date', 'description')


class UserSerializer(ValidateUsernameMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class CurrentUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(ValidateUsernameMixin, serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150, validators=(username_validator(),)
    )


class TokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()