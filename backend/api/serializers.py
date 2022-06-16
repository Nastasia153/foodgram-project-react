from rest_framework import serializers
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredients, RecipeTags
from drf_extra_fields.fields import Base64FileField


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели связи тэга и рецепта."""
    class Meta:
        fields = ('id',)
        model = Tag


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели связи рецепта и ингредиента"""
    id = serializers.PrimaryKeyRelatedField(
        read_only=True, source='ingredient'
    )
    name = serializers.SlugRelatedField(
        read_only=True, slug_field='name', source='ingredient'
    )
    measurement_unit = serializers.SlugRelatedField(
        read_only=True, slug_field='measurement_unit'
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredients


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор на чтение рецепта"""
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
    """Сериализатор на запись рецепта"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientRecipeSerializer(
        read_only=True, many=True, source='ingredient_recipe'
    )
    tags = TagSerializer(read_only=True, many=True)
    image = Base64FileField(required=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'name', 'image', 'ingredients',
            'text', 'cooking_time'
        )
        read_only_fields = ('author',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            current_ingredient, status=Ingredient.objects.get(**ingredient)
            RecipeIngredients.objects.create(
                ingresient=current_ingredient,
                amount=ingredient['amount'],
                recipe=recipe
            )

        for tag in tags:
            current_tag, status=Tag.objects.get(**tag)
            RecipeTags.objects.create(
                tag=current_tag, recipe=recipe
            )
        return recipe
