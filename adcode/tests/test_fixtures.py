from django.core.management import call_command
from django.test import TestCase
try:
    from django.utils.six import StringIO
except ImportError:
    # Django < 1.5. No Python 3 support
    from StringIO import StringIO

from ..models import Size


class FixturesTestCase(TestCase):
    "Ensure that provided fixtures load."

    def test_iab_sizes(self):
        "Load IAB size fixture."
        out = StringIO()
        err = StringIO()
        call_command('loaddata', 'iab_sizes.json', stdout=out, stderr=err)
        self.assertEqual(Size.objects.all().count(), 27)