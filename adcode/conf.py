"Adcode configurations and defaults."
from __future__ import unicode_literals

from django.conf import settings


CONTEXT_KEY_PREFIX = 'ac'

SECTION_CONTEXT_KEY = '{}section'.format(CONTEXT_KEY_PREFIX)

PLACEMENTS_CONTEXT_KEY = '{}placements'.format(CONTEXT_KEY_PREFIX)

PLACEHOLDER_DEFAULT = 'http://placehold.it/{width}x{height}'

if not hasattr(settings, 'ADCODE_PLACEHOLDER_TEMPLATE'):
    settings.ADCODE_PLACEHOLDER_TEMPLATE = PLACEHOLDER_DEFAULT

SECTION_CACHE_KEY = 'alladcodesections'

PLACEMENTS_KEY_FORMAT = 'adcodeplacements{}'

DEFAULT_TIMEOUT = 60 * 60 * 12  # 12 Hours

if not hasattr(settings, 'ADCODE_CACHE_TIMEOUT'):
    settings.ADCODE_CACHE_TIMEOUT = DEFAULT_TIMEOUT
