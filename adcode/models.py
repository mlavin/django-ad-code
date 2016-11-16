"Models for managing site sections and ad placements."
from __future__ import unicode_literals

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from .conf import SECTION_CACHE_KEY, PLACEMENTS_KEY_FORMAT
from .validators import validate_pattern


@python_2_unicode_compatible
class Section(models.Model):
    "A grouping of site urls."

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    pattern = models.CharField(max_length=200, validators=[validate_pattern, ])
    priority = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


def retrieve_all_sections():
    "Get all sections from the cache or query the database."
    sections = cache.get(SECTION_CACHE_KEY, None)
    if sections is None:
        sections = Section.objects.order_by('-priority')
        if settings.ADCODE_CACHE_TIMEOUT:
            sections = list(sections)
            cache.set(SECTION_CACHE_KEY, sections, settings.ADCODE_CACHE_TIMEOUT)
    return sections


@python_2_unicode_compatible
class Size(models.Model):
    "Common Ad size."

    name = models.CharField(max_length=100)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{name} {width}x{height}'.format(
            name=self.name, width=self.width, height=self.height)


@python_2_unicode_compatible
class Placement(models.Model):
    "Ad to be rendered in given sections."

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    remote_id = models.CharField(max_length=200, blank=True, default='')
    size = models.ForeignKey(Size, related_name='placements')
    sections = models.ManyToManyField(Section, blank=True, related_name='placements')

    def __str__(self):
        return '{} ({})'.format(self.name, self.size)

    @property
    def placeholder(self):
        size = {'width': self.width, 'height': self.height}
        return settings.ADCODE_PLACEHOLDER_TEMPLATE.format(**size)

    @property
    def width(self):
        return self.size.width

    @property
    def height(self):
        return self.size.height


def retrieve_section_placements(section):
    "Get all placements for the section from the cache or query the database."
    cache_key = PLACEMENTS_KEY_FORMAT.format(section.pk)
    placements = cache.get(cache_key, None)
    if placements is None:
        placements = Placement.objects.filter(sections=section).select_related('size')
        if settings.ADCODE_CACHE_TIMEOUT:
            placements = list(placements)
            cache.set(cache_key, placements, settings.ADCODE_CACHE_TIMEOUT)
    return placements
