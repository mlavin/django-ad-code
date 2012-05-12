"Template tags to help rendering necessary JS and other markup for displaying ads."

from django import template
from django.conf import settings

from adcode.conf import SECTION_CONTEXT_KEY, PLACEMENTS_CONTEXT_KEY
from adcode.models import Placement

register = template.Library()


class BaseSectionTemplateNode(template.Node):
    """
    Helper class for selecting a set of templates to render based the
    current adcode section.
    """

    def get_current_section(self, context):
        "Grab current section from the context."
        return context.get(SECTION_CONTEXT_KEY, None)

    def get_current_placements(self, context):
        "Grab current placements from the context."
        return context.get(PLACEMENTS_CONTEXT_KEY, None)

    def get_template_list(self, context):
        "Construct list of templates to render. Implemented in subclasses."
        raise NotImplemented() # pragma: no cover

    def get_template_context(self, context):
        "Context passed to the sub-template."
        defaults = {
            'autoescape': context.autoescape,
            'current_app': context.get('current_app', None),
            'use_l10n': context.get('use_l10n', True),
            'use_tz': context.get('use_tz', True),
            'debug': settings.DEBUG,
            'MEDIA_URL': settings.MEDIA_URL,
            'STATIC_URL': settings.STATIC_URL,
        }
        return template.context.Context(defaults)

    def render(self, context):
        "Render a template from a list of possible templates based on the context."
        templates = self.get_template_list(context)
        if templates:
            inner = template.loader.select_template(templates)
            self.nodelist = inner.nodelist
            new_context = self.get_template_context(context)
            return self.nodelist.render(new_context)
        else:
            return ''


class SectionHeaderTemplateNode(BaseSectionTemplateNode):
    "Render section header template for the current section."

    def get_template_context(self, context):
        "Context passed to the sub-template."
        defaults = super(SectionHeaderTemplateNode, self).get_template_context(context)
        defaults['section'] = self.get_current_section(context)
        defaults['placements'] = self.get_current_placements(context)
        return defaults

    def get_template_list(self, context):
        "Build template list from current section"
        section = self.get_current_section(context)
        templates = []
        if section is not None:
            templates = [
                # Section specific header
                u'adcode/{0}/header.html'.format(section.slug),
                # Default template
                u'adcode/header.html'
            ]
        return templates


@register.tag
def render_section_header(parser, token):
    """
    Retrieves the current section from the context and renders the
    appropriate header template. Requires the template to be rendered with
    a RequestContext and 'adcode.context_processors.current_placements' in 
    TEMPLATE_CONTEXT_PROCESSORS.

    Usage: {% render_section_header %}
    """
    return SectionHeaderTemplateNode()


class PlacementTemplateNode(BaseSectionTemplateNode):
    "Render a placement from the current section."

    def __init__(self, slug):
        self.slug = template.Variable(slug)

    def get_current_placement(self, context):
        "Grab current placement from the context."
        placements = self.get_current_placements(context)
        if placements is not None:
            try:
                slug = self.slug.resolve(context)
            except template.VariableDoesNotExist:
                # Fall through to return None
                pass
            else:
                try:
                    placement = placements.get(slug=slug)
                    return placement
                except Placement.DoesNotExist:
                    # Fall through to return None
                    pass
        return None

    def get_template_context(self, context):
        "Context passed to the sub-template."
        defaults = super(PlacementTemplateNode, self).get_template_context(context)
        defaults['section'] = self.get_current_section(context)
        defaults['placement'] = self.get_current_placement(context)
        return defaults

    def get_template_list(self, context):
        "Build template list from current section"
        section = self.get_current_section(context)
        placement = self.get_current_placement(context)
        templates = []
        if section is not None and placement is not None:
            templates = [
                # Placement specific template
                u'adcode/{0}/{1}-placement.html'.format(section.slug, placement.slug),
                # Section specific placement
                u'adcode/{0}/placement.html'.format(section.slug),
                # Default template
                u'adcode/placement.html'
            ]
        return templates


@register.tag
def render_placement(parser, token):
    """
    Retrieves a placement by slug from the context and renders the
    appropriate template. Requires the template to be rendered with
    a RequestContext and 'adcode.context_processors.current_placements' in 
    TEMPLATE_CONTEXT_PROCESSORS.

    Usage: {% render_placement 'header' %}
    """
    try:
        tag_name, slug = token.split_contents()
    except ValueError:
        msg = u"{0} tag requires exactly one argument.".format(token.contents.split())
        raise template.TemplateSyntaxError(msg)
    return PlacementTemplateNode(slug=slug)
