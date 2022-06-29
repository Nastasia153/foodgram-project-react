import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework.serializers import ImageField, ValidationError

IMAGE_UUID4_NAME = '{}.{}'


class Image64Field(ImageField):
    """Поле для декодирования из 64 бит в jpg."""

    def to_internal_value(self, data):
        """Декодирование и сохранение."""
        try:
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name=IMAGE_UUID4_NAME.format(str(uuid.uuid4()), ext))
        except ValueError:
            raise ValidationError({'error': 'Value is invalid'})
        return data
