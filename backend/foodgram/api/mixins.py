from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied


class ValidateUsernameMixin:
    """Проверка отсутствия имени пользователя среди запрещенных"""
    def validate_username(self, value: str):
        if value in settings.RECIPES['RESERVED_USERNAMES']:
            raise serializers.ValidationError(f'Имя {value} зарезервировано')
        return value


class AuthorOnlyMixin:
    """Запрет на узменение и удаление чужого контента"""
    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Невозможно изменить чужой рецепт')
        super().performe_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Нвозможно удалить чужой рецепт')
        super().perform_destroy(instance)
        
        