from django.test import TestCase
from posts.models import Post,User
from django.urls import reverse
from .base import *

class AuthenticationTest(SignUpMixin,UserAndPostFactoryMixin,TestCase):

    def test_sign_up_page_uses_correct_contents(self):
        response = self.client.get(reverse('sign_up'))
        self.assertTemplateUsed(response, 'posts/signUp.html')
        self.assertContains(response, '<form method="POST"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')

    def test_can_submit_the_sign_up_form_and_is_redirected_to_home_being_authenticated(self):
        with self.settings(CAPTCHA_TEST_MODE=True):
            response = self.sign_up()
        
        self.assertEqual(User.objects.all().count(), 3, msg="User object was not created.") #3 because 2 users are created in the factory
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('home'))

    def test_signup_returns_405_if_POST_or_GET_are_NOT_used(self):
        response= self.client.put(reverse('sign_up'))
        self.assertEqual(response.status_code, 405)

        response= self.client.patch(reverse('sign_up'))
        self.assertEqual(response.status_code, 405)


    def test_login_renders_the_correct_template(self):
        response= self.client.get(reverse('login'))
        self.assertTemplateUsed(response,'posts/login.html')

    def test_login_url_has_the_correct_contents(self):
        response= self.client.get(reverse('login'))
        self.assertContains(response, '<form id="login"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password"')

    def test_login_returns_405_if_POST_or_GET_are_NOT_used(self):
        response= self.client.put(reverse('login'))
        self.assertEqual(response.status_code, 405)

        response= self.client.patch(reverse('login'))
        self.assertEqual(response.status_code, 405)    
    
    def test_user_can_not_authenticate_with_incorrect_password(self):
        
        response= self.client.post(reverse('login'),
                        data={'email': 'user1@gmail.com','password': 'wrongpass' })

        self.assertFalse(response.wsgi_request.user.is_authenticated,
                         msg='user is loged in with an incorrect password!')
                
    def test_valid_user_is_redirected_to_home_after_login_in(self):
        response= self.client.post(reverse('login'),
                        data={'email': 'user1@gmail.com','password': '1234' })
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.email, 'user1@gmail.com')
        self.assertTrue(self.user1.check_password('1234'))
        self.assertRedirects(response, reverse('home'))

    def test_logout_redirects_to_login_page_and_logs_out_user(self):
        self.client.login(email= self.user1.email, password='1234')
        response= self.client.get(reverse('logout'))
        
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('login'))


class ErrorHandlingTest(SignUpMixin, TestCase):

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



class HomePageTest(UserAndPostFactoryMixin, TestCase):
    
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

        response= self.client.get(reverse('home'))
        self.assertContains(response, 'class="feed_posts"')
        self.assertContains(response, 'header test2') 
        self.assertContains(response, 'header test1')
    
    def test_home_page_feed_posts_are_ordered_from_newer_to_older(self):

        response= self.client.get(reverse('home'))

        posts_in_context = response.context['posts']
        self.assertEqual(posts_in_context[0].header, 'header test2') #newer post
        self.assertEqual(posts_in_context[1].header, 'header test1')
    
    def test_home_page_returns_405_when_POST_is_used(self):
        response= self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 405)




class PaginationTest(UserAndPostFactoryMixin, TestCase):
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


class CreatePostTest(UserAndPostFactoryMixin, TestCase):

    def test_create_post_button_redirects_loged_out_user_to_signup(self):
        response = self.client.get(reverse('posts:post_form'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('sign_up')))

    def test_create_post_button_renders_a_form_template_correctly_for_a_loged_in_user(self):

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


class PostManagerTest(UserAndPostFactoryMixin, TestCase): 
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
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))


    def test_post_manager_only_displays_the_loged_in_users_posts(self):
        self.client.force_login(self.user2)
        response= self.client.get(reverse('posts:post_manager'))

        self.assertNotContains(response, self.post_obj1.header)
        self.assertContains(response, self.post_obj2.header)



class PostViewTest(UserAndPostFactoryMixin, TestCase):

    def test_post_view_returns_405_if_GET_is_NOT_used(self):
        response= self.client.post(f'{reverse("posts:post_view", args=[self.post_obj1.id])}')
        self.assertEqual(response.status_code, 405)
        
        response= self.client.put(f'{reverse("posts:post_view", args=[self.post_obj1.id])}')
        self.assertEqual(response.status_code, 405)

        response= self.client.patch(f'{reverse("posts:post_view", args=[self.post_obj1.id])}')
        self.assertEqual(response.status_code, 405)

    def test_post_view_displays_correct_post(self):
        response = self.client.get(f'{reverse("posts:post_view", args=[self.post_obj1.id])}')

        self.assertTemplateUsed(response, 'posts/postView.html')
        self.assertEqual(response.context['post'].header, header)
        self.assertEqual(response.context['post'].body, body )
        self.assertContains(response, '<p id="posted_header"')
        self.assertContains(response, '<div id="posted_body"')
    
    def test_post_view_displays_Post_author_and_date(self):
        response = self.client.get(f'{reverse("posts:post_view", args=[self.post_obj1.id])}')

        self.assertContains(response, f'<p id="author">Posted by: {self.user1.username}</p>', html=True) 

        # Test date display - just verify structure exists, not exact format
        self.assertContains(response, '<p id="posted_date">Posted on:')


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
    
    def test_post_views_edit_button_displays_a_prefilled_post_form(self):
        self.client.login(email='user1@gmail.com', password='1234')
        response = self.client.get(reverse('posts:edit_post', args=[self.post_obj1.id]))
        self.assertIn('header test', response.content.decode())
        self.assertIn('body test', response.content.decode())
    
    def test_edit_post_updates_post(self):
        self.client.login(email='user1@gmail.com', password='1234')
        new_header = "Updated Header"
        new_body = "Updated body content"

        response = self.client.post(
            reverse('posts:edit_post', args=[self.post_obj1.id]),
            data={
                'header_input': new_header,
                'body_input': new_body
            }
        )
        self.post_obj1.refresh_from_db()

        self.assertEqual(self.post_obj1.header, new_header)
        self.assertEqual(self.post_obj1.body, new_body)
        self.assertRedirects(response, reverse('posts:post_view', args=[self.post_obj1.id]))

    def test_post_views_edit_button_only_edits_the_post_of_the_author_not_other_users(self):
        self.client.login(email='user1@gmail.com', password='1234')
        response = self.client.get(reverse('posts:edit_post', args=[self.post_obj2.id]), follow=True)
        self.assertContains(response, "You can't edit someone else's post dummy!", html=True)