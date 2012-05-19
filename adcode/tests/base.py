"Test helper functions and base test cases."

import random
import string
import StringIO

from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase

from adcode.models import Section, Size, Placement


class AdCodeDataTestCase(TestCase):
    "Base test case for creating adcode models."

    def tearDown(self):
        cache.clear()

    def get_random_string(self, length=10):
        return u''.join(random.choice(string.ascii_letters) for x in xrange(length))

    def create_section(self, **kwargs):
        "Factory method for creating Sections."
        defaults = {
            'name': self.get_random_string(),
            'slug': self.get_random_string(),
            'pattern': '^/',
        }
        defaults.update(kwargs)
        return Section.objects.create(**defaults)

    def create_size(self, **kwargs):
        "Factory method for creating Sizes."
        defaults = {
            'name': self.get_random_string(),
            'width': random.randint(50, 100),
            'height': random.randint(50, 100),
        }
        defaults.update(kwargs)
        return Size.objects.create(**defaults)

    def create_placement(self, **kwargs):
        "Factory method for creating Placements."
        defaults = {
            'name': self.get_random_string(),
            'slug': self.get_random_string(),
            'remote_id': self.get_random_string(),
        }
        defaults.update(kwargs)
        if 'size' not in defaults:
            defaults['size'] = self.create_size()
        return Placement.objects.create(**defaults)


class FixturesTestCase(TestCase):
    "Ensure that provided fixtures load."

    def test_iab_sizes(self):
        "Load IAB size fixture."
        out = StringIO.StringIO()
        err = StringIO.StringIO()
        call_command('loaddata', 'iab_sizes.json', stdout=out, stderr=err)
        self.assertEqual(Size.objects.all().count(), 27)
