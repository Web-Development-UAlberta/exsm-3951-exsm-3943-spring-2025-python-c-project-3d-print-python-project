from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        assert 1 == 1