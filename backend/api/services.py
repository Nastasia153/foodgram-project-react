"""Модуль вспомогательных функций"""
import string
from random import choices

from django.conf import settings
from django.core.mail import send_mail

SUBJECT = 'Подтверждение регистрации'
MESSAGE = 'Для подтверждения используйте следующий код:\n{code}'


def generate_confirmation_code():
    """Формирование кода подтверждения"""
    return ''.join(choices(
        string.ascii_uppercase + string.digits,
        k=settings.RECIPES['CODE_LENGTH']
    ))


def confirmation_email(address, confirmation_code):
    """Отправка письма с кодом подтверждения"""
    send_mail(
        SUBJECT,
        MESSAGE.format(code=confirmation_code),
        settings.RECIPES['EMAIL_FROM'],
        [address]
    )
