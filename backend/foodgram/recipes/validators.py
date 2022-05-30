from django.core.validators import RegexValidator


def username_validator():
    return RegexValidator(
        regex=r'^[\w.@+-]+$',
        message='Допускаются буквы, цифры и знаки _ @ / + - .'
    )
