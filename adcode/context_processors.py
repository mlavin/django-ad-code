"Context processors for adding current sections and placements in the context."

import re

from .models import Section, Placement


def current_placements(request):
    "Match current section to request path and get related placements."
    # TODO: Add caching
    current = None
    placements = Placement.objects.none()
    sections = Section.objects.all()
    for section in sections:
        pattern = re.compile(section.pattern)
        if pattern.search(request.path):
            current = section
            break
    if current:
        placements = Placement.objects.filter(sections=current).select_related('size')
    return {'adcode-section': current, 'adcode-placements': placements}
