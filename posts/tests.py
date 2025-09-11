from django.test import TestCase

# Create your tests here.

class HomePageTest(TestCase):
    
    def test_home_page_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'posts/home.html')

    def test_home_page_post_button(self):
        response = self.client.get('/')
        self.assertContains(response, '<a href="/posts/new">')
        self.assertContains(response, '<button id="create_post_button">')  

    def test_create_post_button_renders_a_form_template_correctly(self):
        response = self.client.get('/posts/new')
        self.assertTemplateUsed(response, 'posts/postForm.html')
        self.assertContains(response, '<form method="POST"')
        self.assertContains(response, '<input name="header_input"')
        self.assertContains(response, '<input name="body_input"')
        