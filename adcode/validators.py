"Additional model field validators."
from __future__ import unicode_literals

import re

from django.core.exceptions import ValidationError


def validate_pattern(value):
    "Validate value as a valid regular expression."
    try:
        re.compile(value)
    except:
        raise ValidationError('{0} is not a valid regular expression.'.format(value))
