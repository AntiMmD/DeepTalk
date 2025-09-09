from django.test import TestCase
from django.http import HttpRequest
from posts.views import home_page
# Create your tests here.

class HomePageTest(TestCase):
    
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, "<title>Welcome to Monologue!<title>")
        self.assertContains(response.startswith("<html>"))
        self.assertContains(response.endswith("</html>"))