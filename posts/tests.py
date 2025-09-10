from django.test import TestCase
from django.http import HttpRequest
from posts.views import home_page
# Create your tests here.

class HomePageTest(TestCase):
    
    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'posts/home.html')

    def test_home_page_returns_correct_content(self):
        response = self.client.get('/')
        self.assertContains(response, 'Monologue') 