from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Recipe, Ingredient, Tag
from users.models import FoodgramUser


@admin.register(FoodgramUser)
class UserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'is_staff'
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Personal info'),
            {'fields': ('first_name', 'last_name', 'email')}
        ),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


class ChoiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['ingredient']


class IngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    verbose_name = 'связь ингредиент-рецепт'
    verbose_name_plural = 'связи ингредиент-рецепт'


class TagInLine(admin.TabularInline):
    model = Recipe.tags.through
    verbose_name = 'связь ярлык-рецепт'
    verbose_name_plural = 'связи ярлык-рецепт'


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
        'id', 'name', 'text', 'author', 'cooking_time', 'pub_date',
        'get_ingredient', 'get_tag'
    )
    search_fields = ('name__name',)
    inlines = [IngredientInLine, TagInLine]
