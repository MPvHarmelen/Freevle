from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import re

def validate_hex(value):
    hex_error = _('This is an invalid color code. It must be a html hex '
                  'color code e.g. #000000')

    value_length = len(value)

    match = re.match('^\#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', value)
    if value_length != 7 or not match:
        raise ValidationError(hex_error)