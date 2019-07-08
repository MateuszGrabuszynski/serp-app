from django.test import TestCase

from serp_app import utils


class UtilsTestCase(TestCase):
    def test_first_number_from_string_google_like(self):
        self.assertEqual(utils.first_number_from_string('Około 25 500 000 wyników (0,39 s)'), 25500000)

    def test_first_number_from_string_random_good(self):
        self.assertEqual(utils.first_number_from_string('244,394 0 wyniki 239ms'), 2443940)


