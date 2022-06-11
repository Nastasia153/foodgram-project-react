from rest_framework import serializers
from recipes.models import Tag, Ingredient, User, Recipe, RecipeIngredients, RecipeTags
from recipes.validators import username_validator
from .mixins import ValidateUsernameMixin
import base64

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id',)
        model = Tag


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        read_only=True, source='ingredient'
    )
    ingr_name = serializers.SlugRelatedField(
        read_only=True, slug_field='name', source='ingredient'
    )
    measurement_unit = serializers.SlugRelatedField(
        read_only=True, slug_field='measurement_unit'
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredients


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeSerializer(
        read_only=True, many=True, source='ingredient_recipe'
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'name', 'image', 'ingredients',
            'text', 'cooking_time'
        )
        read_only_fields = ('__all__',)


class RecipeWriteSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientRecipeSerializer(
        read_only=True, many=True, source='ingredient_recipe'
    )
    tags = TagSerializer(read_only=True, many=True)
    # image = Base64FileField(required=False, max_length=90000)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'name', 'image', 'ingredients',
            'text', 'cooking_time'
        )
        # read_only_fields = ('author',)

    # def create(self, validated_data):
    #     ingredients = validated_data.pop('ingredients')
    #     tags = validated_data.pop('tags')
    #     recipe = Recipe.objects.create(**validated_data)

    #     for ingredient in ingredients:
    #         current_ingredient, status=Ingredient.objects.get(**ingredient)
    #         RecipeIngredients.objects.create(
    #             ingresient=current_ingredient,
    #             amount=ingredient['amount'],
    #             recipe=recipe
    #         )

    #     for tag in tags:
    #         current_tag, status=Tag.objects.get(**tag)
    #         RecipeTags.objects.create(
    #             tag=current_tag, recipe=recipe
    #         )
    #     return recipe


class UserSerializer(ValidateUsernameMixin, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed')


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
