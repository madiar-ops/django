from django.core.exceptions import ValidationError


def non_negative(value):
    if value < 0:
        raise ValidationError("Значение должно быть положительным числом или 0")
