from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

from .validators import username_validator


class FoodgramUser(AbstractUser):
    """Модель пользователя Foodgram"""
    USER = 'user'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'пользователь'),
        (ADMIN, 'админ'),
    )
    username = models.CharField(
        'имя пользователя',
        max_length=150,
        unique=True,
        validators=(username_validator(),)
    )
    email = models.EmailField('электронная почта', max_length=254, unique=True)
    first_name = models.CharField(
        'имя',
        max_length=150,
        null=True, blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        null=True, blank=True
    )
    bio = models.TextField('о себе', null=True, blank=True)
    role = models.CharField(
        'роль',
        max_length=max(len(key) for key, _ in ROLES),
        choices=ROLES,
        default=USER
    )
    code = models.CharField(max_length=20, null=True, blank=True)

    @property
    def is_admin(self):
        return (
            self.is_staff
            or self.role == FoodgramUser.ADMIN
        )


User = get_user_model()


class Tag(models.Model):
    tag_name = models.CharField(
        'название',
        max_length=16,
    )
    color = models.CharField(
        'цвет',
        max_length=16
    )
    slug = models.SlugField(
        'код',
        unique=True,
        max_length=16
    )

    class Meta:
        default_related_name = 'tags'
        verbose_name = 'ярлык'
        verbose_name_plural = 'ярлыки'

    def colored_tag(self):
        return '<span style="color: #%s;">%s</span>' % (self.color, self.tag_name)

    def __str__(self):
        return self.tag_name


class Ingredient(models.Model):
    ingr_name = models.CharField(
        'ингредиент',
        max_length=150
    )
    measurement_unit = models.CharField(
        'ед.измерения',
        max_length=16
    )

    class Meta:
        default_related_name='ingredients'
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.ingr_name


class Recipe(models.Model):
    title = models.CharField(
        'название',
        max_length=150
    )
    pub_date = models.DateTimeField(
        'дата добавления',
        auto_now_add=True,
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through='Recipe_ingredients'
    )
    image = models.ImageField(
        'картинка',
        upload_to='recipes/',
        blank=True
    )
    cooking_time = models.IntegerField(
        'время приготовления',
        help_text='время в минутах'
    )
    description = models.TextField(
        'описание рецепта'
    )
    tag = models.ManyToManyField(
        Tag,
        through='Recipe_tags'
    )

    class Meta:
        default_related_name = 'recipe'
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def get_ingredient(self):
        return "\n".join([i.ingr_name for i in self.ingredient.all()])

    def get_tag(self):
        return "\n".join([t.tag_name for t in self.tag.all()])

    def __str__(self):
        return self.title


class Recipe_tags(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class Recipe_ingredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        'количество',
        validators=[
            MinValueValidator(1, message='Не меньше 1')
        ],
        default=1
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['ingredient'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredient}, {self.quantity}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор рецепта'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follower'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='check_following'
            )
        ]
        verbose_name = 'подписки'
        verbose_name_plural = 'подписки'


class RecipeBase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт'
    )

    class Meta:
        abstract = True


class Favorite(RecipeBase):
    class Meta(RecipeBase.Meta):
        default_related_name = 'favorite'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]
        verbose_name = 'любимый рецепт'
        verbose_name_plural = 'любимые рецепты'


class Shopping_cart(RecipeBase):
    class Meta(RecipeBase.Meta):
        default_related_name = 'shopping_cart'
        verbose_name = 'список покупок'
        verbose_name_plural = 'список покупок'


# class Shopping_list()
