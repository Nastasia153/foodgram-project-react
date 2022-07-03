from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (
    Favorite, Ingredient, Recipe, RecipeIngredients, ShoppingCart, Tag
)
from users.serializers import UserSerializer


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
    """Сериализатор для модели связи рецепта и ингредиента с количеством."""
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.SlugRelatedField(source='ingredient',
                                        read_only=True,
                                        slug_field='name')
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient', read_only=True, slug_field='measurement_unit')
    amount = serializers.ReadOnlyField()

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор на чтение рецепта."""
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientRecipeSerializer(many=True,
                                             read_only=True,
                                             source='ingredient_recipe')
    author = UserSerializer(read_only=True,
                            default=serializers.CurrentUserDefault())
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)
        read_only_fields = ('__all__',)

    def get_is_favorited(self, obj):
        """Проверка рецепта в разделе Избранное."""
        request = self.context.get('request')
        return request.user.is_authenticated and Favorite.objects.filter(
            user=request.user, recipe__id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверка рецепта в Списке покупок."""
        request = self.context.get('request')
        return request.user.is_authenticated and ShoppingCart.objects.filter(
            user=request.user, recipe__id=obj.id).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор на запись рецепта."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    image = Base64ImageField(use_url=False)

    class Meta:
        model = Recipe
        exclude = ('pub_date',)
        read_only_fields = ('author',)
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=['author', 'name'],
                message='Вы уже разместили рецепт с таким названием')
        ]

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = data.get('tags')
        ingredients_list = []
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_list:
                raise serializers.ValidationError({
                    'detail': 'Игредиенты должны быть уникальными'
                })
            ingredients_list.append(ingredient['id'])
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError({
                    'detail': 'Количество ингрединета должно быть больше 0'
                })
        if len(tags) > len(set(tags)):
            raise serializers.ValidationError({
                'detail: Теги должны быть уникальными'})
        data['ingredients'] = ingredients
        data['tags'] = tags
        return data

    def write_ingredients(self, instance, ingredients):
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
        new_recipe = Recipe.objects.create(**validated_data)
        new_recipe.tags.set(tags)
        self.write_ingredients(new_recipe, ingredients)
        return new_recipe

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
        super().update(instance, validated_data)
        instance.save()
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранного."""
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(read_only=True, source='recipe.image')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины."""
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(read_only=True, source='recipe.image')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')
