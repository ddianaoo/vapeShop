from django.core.exceptions import ValidationError


def validate_phone_length(value):
    if len(value) != 13:
        raise ValidationError('Довжина телефонного номера повинна бути 13 символів.')
    elif '+' not in value:
        raise ValidationError('Невірний формат вводу номера. Введіть за прикладом: +38 *** *** ** **')
