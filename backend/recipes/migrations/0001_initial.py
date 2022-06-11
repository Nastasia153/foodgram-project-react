# Generated by Django 2.2.19 on 2022-06-11 13:57

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodgramUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Допускаются буквы, цифры и знаки _ @ / + - .', regex='^[\\w.@+-]+$')], verbose_name='имя пользователя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='электронная почта')),
                ('first_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='имя')),
                ('last_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='фамилия')),
                ('is_subscribed', models.BooleanField(default=False)),
                ('bio', models.TextField(blank=True, null=True, verbose_name='о себе')),
                ('role', models.CharField(choices=[('user', 'пользователь'), ('admin', 'админ')], default='user', max_length=5, verbose_name='роль')),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='название ингредиента')),
                ('measurement_unit', models.CharField(max_length=16, verbose_name='ед.измерения')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'ингредиенты',
                'default_related_name': 'ingredients',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='название рецепта')),
                ('pub_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='дата добавления')),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/', verbose_name='картинка')),
                ('cooking_time', models.IntegerField(help_text='время в минутах', verbose_name='время приготовления')),
                ('text', models.TextField(verbose_name='описание рецепта')),
                ('is_favorited', models.BooleanField(default=False)),
                ('is_in_shopping_cart', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
                'default_related_name': 'recipes',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='название ярлыка')),
                ('color', models.CharField(max_length=16, verbose_name='цвет')),
                ('slug', models.SlugField(max_length=16, verbose_name='код')),
            ],
            options={
                'verbose_name': 'ярлык',
                'verbose_name_plural': 'ярлыки',
                'default_related_name': 'tags',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to='recipes.Recipe', verbose_name='рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'список покупок',
                'verbose_name_plural': 'список покупок',
                'abstract': False,
                'default_related_name': 'shopping_cart',
            },
        ),
        migrations.CreateModel(
            name='RecipeTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_tag', to='recipes.Recipe')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_tag', to='recipes.Tag')),
            ],
            options={
                'default_related_name': 'recipe_tag',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Не меньше 1')], verbose_name='количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_recipe', to='recipes.Ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_recipe', to='recipes.Recipe')),
            ],
            options={
                'default_related_name': 'ingredient_recipe',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.RecipeIngredients', to='recipes.Ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', through='recipes.RecipeTags', to='recipes.Tag'),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='автор рецепта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='подписчик')),
            ],
            options={
                'verbose_name': 'подписки',
                'verbose_name_plural': 'подписки',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='recipes.Recipe', verbose_name='рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'любимый рецепт',
                'verbose_name_plural': 'любимые рецепты',
                'abstract': False,
                'default_related_name': 'favorite',
            },
        ),
        migrations.AddConstraint(
            model_name='recipeingredients',
            constraint=models.UniqueConstraint(fields=('ingredient',), name='unique_ingredient'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_follower'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, user=django.db.models.expressions.F('author')), name='check_following'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite'),
        ),
    ]
