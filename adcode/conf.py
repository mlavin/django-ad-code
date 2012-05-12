"Adcode configurations and defaults."

from django.conf import settings


CONTEXT_KEY_PREFIX = 'ac'

SECTION_CONTEXT_KEY = '{0}section'.format(CONTEXT_KEY_PREFIX)

PLACEMENTS_CONTEXT_KEY = '{0}placements'.format(CONTEXT_KEY_PREFIX)

PLACEHOLDER_DEFAULT = 'http://placehold.it/{width}x{height}'

PLACEHOLDER_TEMPLATE = getattr(settings, 'ADCODE_PLACEHOLDER_TEMPLATE', PLACEHOLDER_DEFAULT)
