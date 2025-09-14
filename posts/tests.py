from django.test import TestCase
from posts.models import Post
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
    
    def test_can_submit_the_post_form(self):

        header = 'header test'
        body = 'body test'
        response = self.client.post('/posts/new',
                            data={'header_input': header, 'body_input': body})
        
        
        self.assertEqual(Post.objects.count(), 1, msg="Post object was not created. Maybe define the Post model fields?")
        
        post_obj = Post.objects.last()  
        self.assertEqual(post_obj.header, header)
        self.assertEqual(post_obj.body, body)

        redirected_url = f'/posts/posted/{post_obj.id}'
        self.assertRedirects(response, redirected_url)

        response = self.client.get(redirected_url)
        self.assertTemplateUsed(response, 'posts/postView.html')
        self.assertEqual(response.context['header'], header)
        self.assertEqual(response.context['body'], body )
        self.assertContains(response, '<p id="posted_header"')
        self.assertContains(response, '<p id="posted_body"')