from django.test import TestCase
from posts.models import Post,User
from django.urls import reverse
# Create your tests here.

class HomePageTest(TestCase):
    header = 'header test'
    body = 'body test'    

    @staticmethod
    def create_post(header='header test', body= 'body test', amount=1):
        if amount ==1:
            user = User.objects.create(username= 'test',email= 'test@gmail.com')
            post_obj = Post.objects.create(user=user, header=header, body=body)
            return post_obj
        
        usernames = []
        emails= []
        for i in range(0,amount):
            usernames.append(str(i))
            emails.append(f'test{str(i)}@gmail.com')

        users = [User(username=u, email=e) for u, e in zip(usernames, emails)]
        saved_users = User.objects.bulk_create(users)

        posts= [Post(user= user, header= header, body=body) for user in saved_users]
        post_objects = Post.objects.bulk_create(posts)
        return post_objects

    
    def test_home_page_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'posts/home.html')

    def test_home_page_post_button(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, f'<a href="{reverse("post_form")}">')
        self.assertContains(response, '<button id="create_post_button">')  
    
    def test_create_post_button_renders_a_form_template_correctly_for_a_logged_in_user(self):
        user = User.objects.create(email= 'test@gmail.com',username= 'test')
        self.client.force_login(user)
        response = self.client.get(reverse('post_form'))
        self.assertTemplateUsed(response, 'posts/postForm.html')
        self.assertContains(response, '<form method="POST"')
        self.assertContains(response, '<input name="header_input"')
        self.assertContains(response, '<input name="body_input"')
    
    def test_can_submit_the_post_form_and_is_redirected(self):
        user = User.objects.create(email= 'test@gmail.com' ,username= 'test')
        self.client.force_login(user)
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

    def test_can_navigate_to_post_manager(self):
        response= self.client.get(reverse('home'))

        self.assertContains(response, f'<a href="{reverse("post_manager")}"')
    
    def test_post_manager_uses_the_correct_template_and_contents(self):
        post_objects= self.create_post(amount=2)
        response= self.client.get(reverse('post_manager'))

        self.assertTemplateUsed(response, 'posts/postManager.html')
        self.assertContains(response, "<html")
        self.assertContains(response, f'<a href="{reverse("post_view", args=[post_objects[0].id])}"')
        self.assertContains(response, post_objects[0].header)
        self.assertContains(response, f'<a href="{reverse("post_view", args=[post_objects[1].id])}"')
        self.assertContains(response, post_objects[1].header)

    def test_user_can_sign_up(self):
        response = self.client.get(reverse('sign_up'))
        self.assertTemplateUsed(response, 'posts/signUp.html')
        self.assertContains(response, '<form method="POST"')
        self.assertContains(response, '<input name="email_input"')
        self.assertContains(response, '<input name="username_input"')
        self.assertContains(response, '<input name="password_input"')

    def test_can_submit_the_sign_up_form_and_is_redirected_to_home_being_authenticated(self):
        response = self.client.post(reverse('sign_up'),
                                    data={'email_input': 'test@gmail.com',
                                        'username_input':'user',
                                        'password_input':'test'})
        
        self.assertEqual(User.objects.all().count(), 1, msg="User object was not created.")
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('home'))
        


class UserAndPostModelsTest(TestCase):

    def test_each_post_is_associated_with_a_user(self):
        
        user1= User(email= 'user1@gmail.com', username='user1')
        user1.save()
        user2= User(email= 'user2@gmail.com',username='user2')
        user2.save()

        post_obj1 = Post()
        post_obj1.user = user1
        post_obj1.save()

        post_obj2 = Post()
        post_obj2.user = user2
        post_obj2.save()

        saved_post_obj1= Post.objects.get(user= user1 )
        saved_post_obj2= Post.objects.get(user= user2 )
        self.assertEqual(saved_post_obj1, post_obj1)
        self.assertEqual(saved_post_obj2, post_obj2)