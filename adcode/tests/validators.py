"Test custom validation logic."

from django.core.exceptions import ValidationError
from django.utils import unittest

from adcode.validators import validate_pattern


class PatternValidatorTestCase(unittest.TestCase):
    "Validating strings as valid regular expressions."

    def test_valid_patterns(self):
        "Validate expected valid patterns."
        # Average patterns for matching urls
        valid = ['/', '^/$', '/foo', 'bar/', ]
        for pattern in valid:
            self.assertEqual(validate_pattern(pattern), None)

    def test_invalid_patterns(self):
        "Validate known invalid patterns."
        invalid = [
            '(', # Miss matched (
            '*', # Nothing to repeat
            '+', # Nothing to repeat
        ]
        for pattern in invalid:
            self.assertRaises(ValidationError, validate_pattern, pattern)
