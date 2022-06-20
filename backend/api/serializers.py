from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredients,
                            ShoppingCart, Tag)

from api.fields import Image64Field
import users.serializers


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
    """Сериализатор для модели связи рецепта и ингредиента с количеством"""
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()
    amount = serializers.ReadOnlyField()

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор на чтение рецепта"""
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeSerializer(
        read_only=True, many=True, source='ingredient_recipe'
    )
    author = users.serializers.UserSerializer(read_only=True,
                            default=serializers.CurrentUserDefault())
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Image64Field(required=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'name', 'image', 'ingredients',
            'text', 'cooking_time', 'is_favorited', 'is_in_shopping_cart'
        )
        read_only_fields = ('__all__',)

    def get_is_favorited(self, obj):
        """Проверка рецепта в разделе Избранное."""
        if Favorite.objects.filter(recipe=obj.id).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        """Проверка рецепта в Списке покупок."""
        if ShoppingCart.objects.filter(recipe=obj.id).exists():
            return True
        return False


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор на запись рецепта"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    image = Image64Field(required=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'name', 'image', 'ingredients',
            'text', 'cooking_time'
        )
        read_only_fields = ('author',)
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=['author', 'name'],
                message='Вы уже разместили рецепт с таким названием')
        ]

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = []
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError({
                    'detail': 'Игредиенты должны быть уникальными'
                })
            ingredients_list.append(ingredient['id'])
            if int(ingredient['amount']) < 0:
                raise serializers.ValidationError({
                    'detail': 'Количество ингрединета должно быть больше 0'
                })
        data['ingredients'] = ingredients
        return data

    def get_ingredients(self, value):
        """Получение id ингредиента."""
        ingredients_list = IngredientRecipeSerializer(
            value.ingredients.all(), many=True, read_only=True,
            context={'id': value.id}).data
        return ingredients_list

    def write_ingredients(self, ingredients, instance):
        """Запись ингредиентов в БД при создании рецепта."""
        RecipeIngredients.objects.bulk_create([
            RecipeIngredients(recipe=instance,
                              ingredient_id=ingredient.get('id'),
                              amount=ingredient.get('amount'))
            for ingredient in ingredients
        ])

    def create(self, validated_data):
        """Создание рецепта."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = Recipe.objects.create(**validated_data)
        instance.tags.set(tags)
        self.write_ingredients(ingredients, instance)
        return instance

    def update(self, instance, validated_data):
        """Изменение рецепта."""
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.tags.set(validated_data.get('tags', instance.tags))
        instance.ingredients.clear()
        self.write_ingredients(instance, validated_data.pop('ingredients'))
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField(source='pecipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Image64Field(required=False)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')
