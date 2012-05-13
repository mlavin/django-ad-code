"Models for managing site sections and ad placements."

from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .conf import PLACEHOLDER_TEMPLATE, CACHE_TIMEOUT, SECTION_CACHE_KEY
from .validators import validate_pattern


class Section(models.Model):
    "A grouping of site urls."

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    pattern = models.CharField(max_length=200, validators=[validate_pattern, ])
    priority = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return self.name


def retrieve_all_sections():
    "Get all sections from the cache or query the database."
    sections = cache.get(SECTION_CACHE_KEY, None)
    if sections is None:
        sections = list(Section.objects.order_by('-priority'))
        cache.set(SECTION_CACHE_KEY, sections, CACHE_TIMEOUT)
    return sections


@receiver(post_save, sender=Section)
@receiver(post_delete, sender=Section)
def cycle_sections_cache(sender, **kwargs):
    "Delete and restore section info in the cache."
    cache.delete(SECTION_CACHE_KEY)
    retrieve_all_sections()


class Size(models.Model):
    "Common Ad size."

    name = models.CharField(max_length=100)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return u'{0} {1}x{2}'.format(self.name, self.width, self.height)


class Placement(models.Model):
    "Ad to be rendered in given sections."

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    remote_id = models.CharField(max_length=200, blank=True, default=u'')
    size = models.ForeignKey(Size, related_name='placements')
    sections = models.ManyToManyField(Section, blank=True, related_name='placements')

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.size)

    @property
    def placeholder(self):
        size = {'width': self.width, 'height': self.height}
        return PLACEHOLDER_TEMPLATE.format(**size)

    @property
    def width(self):
        return self.size.width

    @property
    def height(self):
        return self.size.height
