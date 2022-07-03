from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import Follow, FoodgramUser
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag, RecipeIngredients


@admin.register(FoodgramUser)
class UserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'role'
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Personal info'),
            {'fields': ('first_name', 'last_name', 'email')}
        ),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'role'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('username', 'email')


class ChoiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['ingredient']


class TagInLine(admin.TabularInline):
    model = Recipe.tags.through
    min_num = 1
    extra = 0
    verbose_name = 'связь ярлык-рецепт'
    verbose_name_plural = 'связи ярлык-рецепт'


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredients
    min_num = 1
    extra = 0


class IngredientAdminForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        widgets = {
            'name': forms.TextInput()
        }
        fields = '__all__'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    form = IngredientAdminForm
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'name', 'author', 'get_tag'
    )
    search_fields = ('name',)
    inlines = [RecipeIngredientInLine, TagInLine]


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('ingredient',
                    'ingredient_id',
                    'recipe',
                    'recipe_id',
                    'amount')
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'author_id')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'recipe_id')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'recipe_id')
