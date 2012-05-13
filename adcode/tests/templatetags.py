"Tests for template tags."

import os

from django.conf import settings
from django.template import Template, TemplateSyntaxError
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.test.client import RequestFactory

from .base import AdCodeDataTestCase
from adcode.conf import SECTION_CONTEXT_KEY, PLACEMENTS_CONTEXT_KEY


class TemplateTagTestCase(AdCodeDataTestCase):
    "Base case to patch TEMPLATE_DIRS while running tests."

    def setUp(self):
        super(TemplateTagTestCase, self).setUp()
        self.template_dirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (
            os.path.join(os.path.dirname(__file__), 'templates'),
        )

    def tearDown(self):
        super(TemplateTagTestCase, self).tearDown()
        settings.TEMPLATE_DIRS = self.template_dirs
        del self.template_dirs


class RenderHeaderTestCase(TemplateTagTestCase):
    "Tag to render current section header."

    def setUp(self):
        super(RenderHeaderTestCase, self).setUp()
        self.factory = RequestFactory()
        self.request = self.factory.get('/foo/')
        self.section = self.create_section(pattern='^/foo/')

    def render_template_tag(self, context=None):
        "Render the template tag."
        context = context or {}
        template = Template("{% load adcode_tags %}{% render_section_header %}")
        context = RequestContext(self.request, {})
        return template.render(context)

    def test_matched_url(self):
        "Successful match of a section to the current url."
        result = self.render_template_tag()
        expected = render_to_string('adcode/header.html', {'section': self.section})
        self.assertEqual(result, expected)

    def test_no_current_section(self):
        "Handle the case where there is no section in the context." 
        self.section.delete()
        result = self.render_template_tag()
        self.assertEqual(result, u'')

    def test_section_specific_template(self):
        "Tag should use section specific template if available."
        self.section.slug = 'section-1'
        self.section.save()
        result = self.render_template_tag()
        expected = render_to_string('adcode/section-1/header.html', {'section': self.section})
        self.assertEqual(result, expected)


class RenderPlacementTestCase(TemplateTagTestCase):
    "Tag to render ad placement header."

    def setUp(self):
        super(RenderPlacementTestCase, self).setUp()
        self.factory = RequestFactory()
        self.request = self.factory.get('/foo/')
        self.section = self.create_section(pattern='^/foo/')
        self.placement = self.create_placement(slug='footer')
        self.placement.sections.add(self.section)

    def render_template_tag(self, slug='"footer"', context=None):
        "Render the template tag."
        context = context or {}
        template = Template("{{% load adcode_tags %}}{{% render_placement {0} %}}".format(slug))
        context = RequestContext(self.request, context)
        return template.render(context)

    def test_basic_rendering(self):
        "Render a placement by the slug."
        result = self.render_template_tag()
        context = {'section': self.section, 'placement': self.placement}
        expected = render_to_string('adcode/placement.html',context)
        self.assertEqual(result, expected)

    def test_no_current_section(self):
        "Handle the case where there is no section in the context." 
        self.section.delete()
        result = self.render_template_tag()
        self.assertEqual(result, u'')

    def test_no_matched_placement(self):
        "Handle the case where there is placement matching the slug." 
        self.placement.delete()
        result = self.render_template_tag()
        self.assertEqual(result, u'')

    def test_section_specific_template(self):
        "Tag should use section specific template if available."
        self.section.slug = 'section-1'
        self.section.save()
        result = self.render_template_tag()
        context = {'section': self.section, 'placement': self.placement}
        expected = render_to_string('adcode/section-1/placement.html',context)
        self.assertEqual(result, expected)

    def test_placement_specific_template(self):
        "Tag should use section specific template if available."
        self.section.slug = 'section-1'
        self.section.save()
        self.placement.slug = 'sidebar'
        self.placement.save()
        result = self.render_template_tag(slug='"sidebar"')
        context = {'section': self.section, 'placement': self.placement}
        expected = render_to_string('adcode/section-1/sidebar-placement.html', context)
        self.assertEqual(result, expected)

    def test_variable_slug_name(self):
        "Pass a variable for the slug name rather than a string."
        result = self.render_template_tag(slug='var', context={'var': 'footer'})
        context = {'section': self.section, 'placement': self.placement}
        expected = render_to_string('adcode/placement.html',context)
        self.assertEqual(result, expected)

    def test_unknown_variable(self):
        "Gracefully handle unknown variable given."
        result = self.render_template_tag(slug='var', context={})
        context = {'section': self.section, 'placement': self.placement}
        self.assertEqual(result, '')

    def test_no_slug_given(self):
        "Raises TemplateSyntaxError if no slug is given."
        self.assertRaises(TemplateSyntaxError, self.render_template_tag, slug='')
