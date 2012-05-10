"Template tags to help rendering necessary JS and other markup for displaying ads."

from django import template
from django.conf import settings

from .conf import SECTION_CONTEXT_KEY, PLACEMENTS_CONTEXT_KEY

register = template.Library()


class BaseSectionTemplateNode(template.Node):
    """
    Helper class for selecting a set of templates to render based the
    current adcode section.
    """

    def get_current_section(self, context):
        "Grab current section from the context."
        return context.get(SECTION_CONTEXT_KEY, None)

    def get_template_list(self, context):
        "Construct list of templates to render. Implemented in subclasses."
        raise NotImplemented()

    def get_template_context(self, context):
        "Context passed to the sub-template."
        return {}

    def render(self, context):
        "Render a template from a list of possible templates based on the context."
        templates = self.get_template_list(context)
        if templates:
            inner = loader.select_template(templates)
            self.nodelist = inner.nodelist
            new_context = self.get_template_context(context)
            return self.nodelist.render(new_context)
        else:
            return ''


class SectionHeaderTemplateNode(BaseSectionTemplateNode):
    "Render section header template for the current section."

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
