from django.test import TestCase
from posts.models import Post,User
from django.urls import reverse

header = 'header test'
body = 'body test'    
def create_post(user, header=header, body= body, amount=1):
    if amount ==1:
        post_obj = Post.objects.create(user=user, header=header, body=body)
        return post_obj
    
    posts= [Post(user= user, header= header, body=body) for _ in range(0,amount)]
    post_objects = Post.objects.bulk_create(posts)
    return post_objects



class UserAndPostFactory(TestCase):
    def setUp(self):
        self.user1= User.objects.create_user(email= 'user1@gmail.com', username='user1',password='1234')
        self.user2= User.objects.create_user(email= 'user2@gmail.com',username='user2',password='1234')

        self.post_obj1= create_post(user=self.user1)
        self.post_obj2 = create_post(user=self.user2, header='test2', body='test2')



class AuthenticationTest(TestCase):

    def sign_up(self, email='test@gmail.com', username='test', password= 'test',captcha_1= 'passed'):
        with self.settings(CAPTCHA_TEST_MODE=True):
            response = self.client.post(reverse('sign_up'),
                                        data={'email': email,
                                            'username':username,
                                            'password':password,
                                            'captcha_0': 'dummy',
                                            'captcha_1':captcha_1})
            return response

    def test_sign_up_page_uses_correct_contents(self):
        response = self.client.get(reverse('sign_up'))
        self.assertTemplateUsed(response, 'posts/signUp.html')
        self.assertContains(response, '<form method="POST"')
        self.assertContains(response, 'name="email_input"')
        self.assertContains(response, 'name="username_input"')
        self.assertContains(response, 'name="password_input"')

    def test_can_submit_the_sign_up_form_and_is_redirected_to_home_being_authenticated(self):
        with self.settings(CAPTCHA_TEST_MODE=True):
            response = self.sign_up()
        
        self.assertEqual(User.objects.all().count(), 1, msg="User object was not created.")
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('home'))

    def test_login_renders_the_correct_template(self):
        response= self.client.get(reverse('login'))
        self.assertTemplateUsed(response,'posts/login.html')

    def test_login_url_has_the_correct_contents(self):
        response= self.client.get(reverse('login'))
        self.assertContains(response, '<form id="login"')
        self.assertContains(response, 'name="email_input"')
        self.assertContains(response, 'name="password_input"')
    

    def test__user_can_not_authenticate_with_incorrect_password(self):
        User.objects.create_user(email='test@gmail.com', username= 'test', password='test1234')
        
        response= self.client.post(reverse('login'),
                        data={'email_input': 'test@gmail.com','password_input': 'wrongpass' })

        self.assertFalse(response.wsgi_request.user.is_authenticated,
                         msg='user is loged in with an incorrect password!')
                
    def test_valid_user_is_redirected_to_home_after_login_in(self):
        User.objects.create_user(email='test@gmail.com', username= 'test', password='test1234')
        user = User.objects.get(email='test@gmail.com')

        response= self.client.post(reverse('login'),
                        data={'email_input': 'test@gmail.com','password_input': 'test1234' })
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.email, 'test@gmail.com')
        self.assertTrue(user.check_password('test1234'))
        self.assertRedirects(response, reverse('home'))



class ErrorHandlingTest(AuthenticationTest):

    def test_sign_up_view_displays_captcha_error_when_the_captcha_is_filled_incorrectly(self):
            response = self.sign_up(captcha_1='NOTpassed')                
            self.assertContains(response, 'Invalid CAPTCHA')
                

    def test_user_is_informed_that_the_email_theyre_using_is_duplicant_when_only_the_email_is_duplicated(self):
        self.sign_up() 

        response = self.sign_up(username= 'smthElse')
        self.assertTemplateUsed(response, 'posts/signUp.html')
        self.assertContains(response, 'A user with this email already exists!')
        self.assertNotContains(response, 'This username is taken!') 

    def test_user_is_informed_that_the_username_theyre_using_is_duplicant_when_only_the_username_is_duplicated(self):
        self.sign_up() 

        response= self.sign_up(email='differentemail@gmail.com')   
        self.assertTemplateUsed(response, 'posts/signUp.html') 
        self.assertContains(response, 'This username is taken!') 
        self.assertNotContains(response, 'A user with this email already exists!')

    def test_user_is_informed_that_the_username_and_email_theyre_using_is_duplicant_when_both_are_duplicated(self):
        self.sign_up() 

        response= self.sign_up()
        self.assertTemplateUsed(response, 'posts/signUp.html')
        self.assertContains(response, 'A user with this email already exists!')
        self.assertContains(response, 'This username is taken!') 



class HomePageTest(AuthenticationTest):
    
    def test_home_page_uses_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'posts/home.html')

    def test_home_page_post_button(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, reverse("posts:post_form"))
        self.assertContains(response, '<button id="create_post_button">')      

    def test_can_navigate_to_post_manager(self):
        response= self.client.get(reverse('home'))

        self.assertContains(response, f'<a href="{reverse("posts:post_manager")}"')

    def test_home_page_feed_displays_users_posts(self):
        user1 = User.objects.create_user(username='Farshad', email='Farshad@gmail.com')
        user2 = User.objects.create_user(username='Sara', email='Sara@gmail.com')

        create_post(user= user1, header= 'Puppies are the best')
        create_post(user= user2, header= 'Kitties are the best')

        response= self.client.get(reverse('home'))
        self.assertContains(response, 'class="feed_post"')
        self.assertContains(response, 'Puppies are the best')
        self.assertContains(response, 'Kitties are the best')
    
    def test_home_page_feed_posts_are_ordered_from_newer_to_older(self):
        user1 = User.objects.create_user(username='Farshad', email='Farshad@gmail.com')
        user2 = User.objects.create_user(username='Sara', email='Sara@gmail.com')

        create_post(user= user1, header= 'Old Post')
        create_post(user= user2, header= 'New Post')
        response= self.client.get(reverse('home'))

        posts_in_context = response.context['posts']
        self.assertEqual(posts_in_context[0].header, 'New Post')
        self.assertEqual(posts_in_context[1].header, 'Old Post')



class PaginationTest(UserAndPostFactory):
    """Test pagination behavior without hardcoding page size"""
    
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            email='pagtest@gmail.com', 
            username='pagtest'
        )

        create_post(user=self.user, amount=60)
    
    def test_home_page_displays_pagination_controls(self):
        response = self.client.get(reverse('home'))
        
        self.assertContains(response, '<nav>')
        self.assertContains(response, 'class="pagination"')
        
        self.assertContains(response, '?page=')

    def test_pagination_respects_page_parameter(self):
        """Different pages show different content"""
        response_page1 = self.client.get(reverse('home') + '?page=1')
        response_page2 = self.client.get(reverse('home') + '?page=2')
        
        posts_page1 = set(p.id for p in response_page1.context['posts'])
        posts_page2 = set(p.id for p in response_page2.context['posts'])
        
        # Pages should not overlap
        self.assertEqual(len(posts_page1.intersection(posts_page2)), 0,
                        "Pages should display different posts")



class CreatePostTest(UserAndPostFactory):

    def test_create_post_button_redirects_logged_out_user_to_signup(self):
        response = self.client.get(reverse('posts:post_form'))
        self.assertRedirects(response, reverse('sign_up'))

    def test_create_post_button_renders_a_form_template_correctly_for_a_logged_in_user(self):

        self.client.force_login(self.user1)
        response = self.client.get(reverse('posts:post_form'))
        self.assertTemplateUsed(response, 'posts/postForm.html')
        self.assertContains(response, '<form method="POST"')
        self.assertContains(response, '<input name="header_input"')
        self.assertContains(response, '<textarea name="body_input"')
    
    def test_can_submit_the_post_form_and_is_redirected(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('posts:post_form'),
                            data={'header_input': header, 'body_input': body})
        
        self.assertEqual(Post.objects.count(), 3, msg="Post object was not created. Maybe define the Post model fields?")
        
        post_obj = Post.objects.first() # because Post model's queryset ordering is set to ['-created_at']

        self.assertEqual(post_obj.header, header)
        self.assertEqual(post_obj.body, body)
        self.assertRedirects(response, f'{reverse("posts:post_view", args=[post_obj.id])}')
        


class PostManagerTest(UserAndPostFactory): 
    def test_post_manager_uses_the_correct_template(self):
        self.client.force_login(self.user1)
        response= self.client.get(reverse('posts:post_manager'))

        self.assertTemplateUsed(response, 'posts/postManager.html')

    def test_post_manager_has_the_correct_contents(self):
        self.client.force_login(self.user1)
        #the first post_obj of this user is already created in the factory
        post_obj2= create_post(user=self.user1, header='second post')
        response= self.client.get(reverse('posts:post_manager'))

        self.assertContains(response, "<html")
        self.assertContains(response, f'<a href="{reverse("posts:post_view", args=[self.post_obj1.id])}"')
        self.assertContains(response, self.post_obj1.header)
        self.assertContains(response, f'<a href="{reverse("posts:post_view", args=[post_obj2.id])}"')
        self.assertContains(response,post_obj2.header)

    def test_post_manager_redirects_to_login_page_if_user_is_loged_out(self):
        response= self.client.get(reverse('posts:post_manager'))

        self.assertRedirects(response, reverse('login'))

    def test_post_manager_only_displays_the_logged_in_users_posts(self):
        self.client.force_login(self.user2)
        response= self.client.get(reverse('posts:post_manager'))

        self.assertNotContains(response, self.post_obj1.header)
        self.assertContains(response, self.post_obj2.header)



class PostViewTest(UserAndPostFactory):
    def test_post_view_displays_correct_post(self):
        response = self.client.get(f'{reverse("posts:post_view", args=[self.post_obj1.id])}')

        self.assertTemplateUsed(response, 'posts/postView.html')
        self.assertEqual(response.context['post'].header, header)
        self.assertEqual(response.context['post'].body, body )
        self.assertContains(response, '<p id="posted_header"')
        self.assertContains(response, '<p id="posted_body"')
    
    def test_post_view_allows_navigation_back_home(self):
        response = self.client.get(f'{reverse("posts:post_view", args=[self.post_obj1.id])}')

        self.assertContains(response, f'<a href="{reverse("home")}"')
        self.assertContains(response,'id="home_redirect"')
    
    def test_post_view_has_delete_button(self):
        response = self.client.get(f'{reverse("posts:post_view", args=[self.post_obj1.id])}')
        self.assertContains(response, f'<button id="delete_post"')
    
    def test_post_views_delete_button_redirects_to_post_manager_page(self):
        self.client.login(email='user1@gmail.com', password='1234')
        response = self.client.post(reverse('posts:delete_post', args=[self.post_obj1.id]))
        self.assertRedirects(response, reverse('posts:post_manager'))

    def test_post_views_delete_button_deletes_the_post(self):
        self.client.login(email='user1@gmail.com', password='1234')
        response = self.client.post(reverse('posts:delete_post', args=[self.post_obj1.id]), follow=True)
        self.assertNotContains(response, self.post_obj1.header)
        self.assertFalse(Post.objects.filter(id=self.post_obj1.id).exists()) 

    def test_post_views_delete_button_only_deletes_the_post_of_the_author_not_other_users(self):
        self.client.login(email='user1@gmail.com', password='1234')
        response = self.client.post(reverse('posts:delete_post', args=[self.post_obj2.id]), follow=True)
        self.assertTrue(Post.objects.filter(id=self.post_obj2.id).exists()) 
        self.assertContains(response, "You can't delete someone else's post dummy!", html=True)




class UserAndPostModelsTest(UserAndPostFactory):
    def test_each_post_is_associated_with_a_user(self):
        saved_post_obj1= Post.objects.get(user= self.user1 )
        saved_post_obj2= Post.objects.get(user= self.user2 )
        self.assertEqual(saved_post_obj1, self.post_obj1)
        self.assertEqual(saved_post_obj2,self. post_obj2)

    def test_post_has_a_created_at_field(self):
        self.assertGreater(self.post_obj2.created_at, self.post_obj1.created_at)