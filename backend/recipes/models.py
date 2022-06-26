from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('название ярлыка', max_length=16,)
    color = models.CharField('цвет', max_length=16)
    slug = models.SlugField('код', max_length=16)

    class Meta:
        default_related_name = 'tags'
        verbose_name = 'ярлык'
        verbose_name_plural = 'ярлыки'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('название ингредиента', max_length=150)
    measurement_unit = models.CharField('ед.измерения', max_length=16)

    class Meta:
        default_related_name = 'ingredients'
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField('название рецепта', max_length=150)
    pub_date = models.DateTimeField(
        'дата добавления', auto_now_add=True, null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='автор'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients'
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True, null=True,
        verbose_name='картинка'
    )
    cooking_time = models.IntegerField(
        'время приготовления',
        validators=[MinValueValidator(1, message='Не меньше 1')],
        default=1, help_text='минут'
    )
    text = models.TextField('описание рецепта')
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTags'
    )

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['-pub_date']

    def get_ingredient(self):
        return "\n".join([i.name for i in self.ingredients.all()])

    def get_tag(self):
        return "\n".join([t.name for t in self.tags.all()])

    def __str__(self):
        return self.name


class RecipeTags(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = 'recipe_tag'
        constraints = [
            UniqueConstraint(
                fields=['tag', 'recipe'],
                name='unique_tag_recipe'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        'количество',
        validators=[
            MinValueValidator(1, message='Не меньше 1')
        ],
        default=1
    )

    class Meta:
        default_related_name = 'ingredient_recipe'

    def __str__(self):
        return f'{self.recipe} {self.ingredient} {self.amount}'


class RecipeBase(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='рецепт'
    )

    class Meta:
        abstract = True
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]


class Favorite(RecipeBase):
    class Meta(RecipeBase.Meta):
        default_related_name = 'favorite'
        verbose_name = 'любимый рецепт'
        verbose_name_plural = 'любимые рецепты'


class ShoppingCart(RecipeBase):
    class Meta(RecipeBase.Meta):
        default_related_name = 'shopping_cart'
        verbose_name = 'список покупок'
        verbose_name_plural = 'список покупок'
