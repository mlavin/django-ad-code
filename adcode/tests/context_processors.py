"Tests for context processors."

from django.test.client import RequestFactory

from .base import AdCodeDataTestCase
from adcode.conf import SECTION_CONTEXT_KEY, PLACEMENTS_CONTEXT_KEY
from adcode.context_processors import current_placements


class CurrentPlacementsTestCase(AdCodeDataTestCase):
    "Test matching sections/placements for the current url."

    def setUp(self):
        self.factory = RequestFactory()

    def test_matched_url(self):
        "Successful match of a section to the current url."
        request = self.factory.get('/foo/')
        section = self.create_section(pattern='^/foo/')
        context = current_placements(request)
        self.assertEqual(context[SECTION_CONTEXT_KEY], section)

    def test_no_matched_urls(self):
        "Handle when no sections match the current url."
        request = self.factory.get('/foo/')
        section = self.create_section(pattern='^/bar/')
        context = current_placements(request)
        self.assertEqual(context[SECTION_CONTEXT_KEY], None)

    def test_no_existing_sections(self):
        "Handle when no sections are defined."
        request = self.factory.get('/foo/')
        context = current_placements(request)
        self.assertEqual(context[SECTION_CONTEXT_KEY], None)

    def test_match_url_placements(self):
        "Successful match of placements for the current url."
        request = self.factory.get('/foo/')
        section = self.create_section(pattern='^/foo/')
        placement = self.create_placement()
        placement.sections.add(section)
        context = current_placements(request)
        placements = context[PLACEMENTS_CONTEXT_KEY]
        self.assertEqual(placements.count(), 1)
        self.assertTrue(placement in placements)

    def test_match_url_no_placements(self):
        "Handle no placements for the match url."
        request = self.factory.get('/foo/')
        section = self.create_section(pattern='^/foo/')
        context = current_placements(request)
        placements = context[PLACEMENTS_CONTEXT_KEY]
        self.assertEqual(placements.count(), 0)
