"Performance related tests."

from django.core.cache import cache
from django.template import Template
from django.template.context import RequestContext
from django.test.client import RequestFactory


from .templatetags import TemplateTagTestCase
from adcode.conf import SECTION_CONTEXT_KEY, PLACEMENTS_CONTEXT_KEY
from adcode.context_processors import current_placements


class QueryCountsTestCase(TemplateTagTestCase):
    "Tracking number of queries executed."

    def setUp(self):
        super(QueryCountsTestCase, self).setUp()
        self.factory = RequestFactory()
        self.request = self.factory.get('/foo/')
        self.section = self.create_section(pattern='^/foo/')
        self.placement = self.create_placement()
        self.placement.sections.add(self.section)

    def tearDown(self):
        cache.clear()

    def test_context_processor(self):
        "Number of queries for the context processor with no cache."
        with self.assertNumQueries(1):
            # Single query to get check path vs. section patterns
            context = current_placements(self.request)

    def test_render_header(self):
        "Number of queries to render header with no cache."
        template = Template("{% load adcode_tags %}{% render_section_header %}")
        context = RequestContext(self.request, {})
        with self.assertNumQueries(0):
            # No additional queries to header which does not access placements
            template.render(context)

    def test_render_placement(self):
        "Number of queries to render a placement with no cache."
        template = Template(
            "{{% load adcode_tags %}}{{% render_placement '{0}' %}}".format(self.placement.slug)
        )
        context = RequestContext(self.request, {})
        with self.assertNumQueries(1):
            # One query to fetch placement from context
            template.render(context)
