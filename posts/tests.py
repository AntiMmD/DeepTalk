from django.test import TestCase
from posts.models import Post
from django.urls import reverse
# Create your tests here.

class HomePageTest(TestCase):

    header = 'header test'
    body = 'body test'    

    @staticmethod
    def create_post(header='header test', body= 'body test', amount=1):
        if amount ==1:
            post_obj = Post.objects.create(header=header, body=body)
            return post_obj

        posts= [Post(header= header, body=body) for _ in range(0,amount)]
        
        post_objects = Post.objects.bulk_create(posts)
        return post_objects

    
    def test_home_page_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'posts/home.html')

    def test_home_page_post_button(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, f'<a href="{reverse("post_form")}">')
        self.assertContains(response, '<button id="create_post_button">')  

    def test_create_post_button_renders_a_form_template_correctly(self):
        response = self.client.get(reverse('post_form'))
        self.assertTemplateUsed(response, 'posts/postForm.html')
        self.assertContains(response, '<form method="POST"')
        self.assertContains(response, '<input name="header_input"')
        self.assertContains(response, '<input name="body_input"')
    
    def test_can_submit_the_post_form_and_is_redirected(self):

        response = self.client.post(reverse('post_form'),
                            data={'header_input': self.header, 'body_input': self.body})
        
        self.assertEqual(Post.objects.count(), 1, msg="Post object was not created. Maybe define the Post model fields?")
        
        post_obj = Post.objects.last()  

        self.assertEqual(post_obj.header, self.header)
        self.assertEqual(post_obj.body, self.body)
        self.assertRedirects(response, f'{reverse("post_view", args=[post_obj.id])}')

    def test_post_view_displays_correct_post(self):

        post_obj = self.create_post()
        response = self.client.get(f'{reverse("post_view", args=[post_obj.id])}')

        self.assertTemplateUsed(response, 'posts/postView.html')
        self.assertEqual(response.context['header'], self.header)
        self.assertEqual(response.context['body'], self.body )
        self.assertContains(response, '<p id="posted_header"')
        self.assertContains(response, '<p id="posted_body"')
    
    def test_post_view_allows_navigation_back_home(self):

        post_obj = self.create_post()
        response = self.client.get(f'{reverse("post_view", args=[post_obj.id])}')
        self.assertContains(response, f'<a href="{reverse("home")}"')
        self.assertContains(response,'id="home_redirect"')

    def test_can_navigate_to_posts_manager(self):
        post_objects= self.create_post(amount=2)
        response= self.client.get(reverse('home'))

        self.assertContains(response, f'<a href="{reverse("post_manager")}"')

        
        response= self.client.get(reverse('post_manager'))
        self.assertTemplateUsed(response, 'posts/postManager.html')
        self.assertContains(response, "<html")
        self.assertContains(response, f'<a href="{reverse("post_view", args=[post_objects[0].id])}"')
        self.assertContains(response, post_objects[0].header)
        self.assertContains(response, f'<a href="{reverse("post_view", args=[post_objects[1].id])}"')
        self.assertContains(response, post_objects[1].header)
        
