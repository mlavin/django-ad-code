"Adcode configurations and defaults."

from django.conf import settings


CONTEXT_KEY_PREFIX = 'ac'

SECTION_CONTEXT_KEY = '{0}section'.format(CONTEXT_KEY_PREFIX)

PLACEMENTS_CONTEXT_KEY = '{0}placements'.format(CONTEXT_KEY_PREFIX)

PLACEHOLDER_DEFAULT = 'http://placehold.it/{width}x{height}'

PLACEHOLDER_TEMPLATE = getattr(settings, 'ADCODE_PLACEHOLDER_TEMPLATE', PLACEHOLDER_DEFAULT)

SECTION_CACHE_KEY = 'alladcodesections'

PLACEMENTS_KEY_FORMAT = 'adcodeplacements{0}'

DEFAULT_TIMEOUT = 60 * 60 * 12  # 12 Hours

CACHE_TIMEOUT = getattr(settings, 'ADCODE_CACHE_TIMEOUT', DEFAULT_TIMEOUT)
