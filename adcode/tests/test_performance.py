"Performance related tests."
from __future__ import unicode_literals

from django.core.cache import cache
from django.template import Template
from django.template.context import RequestContext
from django.test import override_settings
from django.test.client import RequestFactory

from .test_templatetags import TemplateTagTestCase
from ..context_processors import current_placements


@override_settings(ADCODE_CACHE_TIMEOUT=10)
class QueryCountsTestCase(TemplateTagTestCase):
    "Tracking number of queries executed."

    def setUp(self):
        super(QueryCountsTestCase, self).setUp()
        self.factory = RequestFactory()
        self.request = self.factory.get('/foo/')
        self.section = self.create_section(pattern='^/foo/')
        self.placement = self.create_placement()
        self.placement.sections.add(self.section)

    def test_context_processor_no_cache(self):
        "Number of queries for the context processor with no cache."
        cache.clear()
        with self.assertNumQueries(2):
            # One query to get all current sections
            # One query to get all placements the current section
            current_placements(self.request)

    def test_context_processor_cached(self):
        "Subsequent calls through the context process should be cached."
        current_placements(self.request)
        with self.assertNumQueries(0):
            request = self.factory.get('/foo/')
            current_placements(request)

    def test_context_processor_new_section(self):
        "Subsequent calls with a new section only require querying the placements."
        self.create_section(pattern='^/bar/')
        current_placements(self.request)
        with self.assertNumQueries(1):
            request = self.factory.get('/bar/')
            current_placements(request)

    def test_render_header_no_cache(self):
        "Number of queries to render header with no cache."
        template = Template("{% load adcode_tags %}{% render_section_header %}")
        context = RequestContext(self.request, {})
        cache.clear()
        with self.assertNumQueries(2):
            # As of Django 1.8 the context processors are evaluated at render time.
            # This should have the same number of queries as the context processor.
            # No additional queries to header which does not access placements.
            template.render(context)

    def test_render_placement_no_cache(self):
        "Number of queries to render a placement with no cache."
        template = Template(
            "{{% load adcode_tags %}}{{% render_placement '{0}' %}}".format(self.placement.slug)
        )
        context = RequestContext(self.request, {})
        cache.clear()
        with self.assertNumQueries(2):
            # As of Django 1.8 the context processors are evaluated at render time.
            # This should have the same number of queries as the context processor.
            # All queries are executed and cached in the context processor
            template.render(context)

    def test_render_placement_cached(self):
        "Subsequent placement renders should be cached."
        template = Template(
            "{{% load adcode_tags %}}{{% render_placement '{0}' %}}".format(self.placement.slug)
        )
        context = RequestContext(self.request, {})
        template.render(context)
        with self.assertNumQueries(0):
            template.render(context)

    def test_multiple_placements_same_section(self):
        "Mutliple placements in the same section should be cached."
        other_placement = self.create_placement()
        other_placement.sections.add(self.section)
        template = Template(
            """
            {{% load adcode_tags %}}
            {{% render_placement '{0}' %}}
            {{% render_placement '{1}' %}}
            """.format(self.placement.slug, other_placement.slug)
        )
        context = RequestContext(self.request, {})
        cache.clear()
        with self.assertNumQueries(2):
            # As of Django 1.8 the context processors are evaluated at render time.
            # This should have the same number of queries as the context processor.
            # All queries are executed and cached in the context processor
            template.render(context)
