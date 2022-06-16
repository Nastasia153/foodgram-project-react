from django.conf import settings
from rest_framework import serializers


class ValidateUsernameMixin:
    """Проверка отсутствия имени пользователя среди запрещенных"""
    def validate_username(self, value: str):
        if value in settings.RECIPES['RESERVED_USERNAMES']:
            raise serializers.ValidationError(f'Имя {value} зарезервировано')
        return value
