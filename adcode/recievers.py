from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from .conf import SECTION_CACHE_KEY, PLACEMENTS_KEY_FORMAT
from .models import Section, Placement, retrieve_all_sections


@receiver(post_save, sender=Section)
@receiver(post_delete, sender=Section)
def cycle_sections_cache(sender, **kwargs):
    "Delete and restore section info in the cache."
    cache.delete(SECTION_CACHE_KEY)
    if settings.ADCODE_CACHE_TIMEOUT:
        retrieve_all_sections()


def _update_placement_cache(placement, replace=True):
    "Remove placement from related section caches. Replace if requested."
    if settings.ADCODE_CACHE_TIMEOUT:
        for section in placement.sections.all():
            cache_key = PLACEMENTS_KEY_FORMAT.format(section.pk)
            placements = cache.get(cache_key, [])
            try:
                placements.remove(placement)
            except ValueError:
                # Placement not in the list
                pass
            if replace:
                placements.append(placement)
            cache.set(cache_key, placements, settings.ADCODE_CACHE_TIMEOUT)


@receiver(post_save, sender=Placement)
def save_placement_handler(sender, instance,  **kwargs):
    "Add or update the placement in the caches."
    _update_placement_cache(placement=instance, replace=True)


@receiver(pre_delete, sender=Placement)
def delete_placement_handler(sender, instance,  **kwargs):
    "Remove the placement from the section caches."
    _update_placement_cache(placement=instance, replace=False)
