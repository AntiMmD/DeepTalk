import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from urllib.parse import urlparse
from posts.models import Post
from django.contrib.auth import get_user_model
User = get_user_model()

        # Farshad has recently heard about a cool website where he can write a blog post and share it with others
        # he opens his browser and checks the homepage 

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        if test_server := os.environ.get("TEST_SERVER"):   
            self.live_server_url = "http://" + test_server

    def tearDown(self):
        self.browser.quit()

    def login(self,email= 'test@gmail.com', password='test1234'):
        
        self.browser.get(self.live_server_url + reverse('login'))

        email_input= self.browser.find_element(By.ID, "email_input")
        password_input= self.browser.find_element(By.ID, "password_input")
                
        email_input.send_keys(email)
        password_input.send_keys(password)
        self.browser.find_element(By.ID, "submit").click()

    def sign_up(self,email= 'test@gmail.com',username= 'test',password='test1234'):

        ## remember to set CAPTCHA_TEST_MODE=True in the settings when testing
        ## REMOVE IT IN PRODUCTION
        with self.settings(CAPTCHA_TEST_MODE=True):
            self.browser.get(f'{self.live_server_url}{reverse('sign_up')}')
            email_input= self.browser.find_element(By.ID, "email_input")
            username_input= self.browser.find_element(By.ID, "username_input")
            password_input= self.browser.find_element(By.ID, "password_input")
            
            self.browser.find_element(By.NAME, "captcha_1").send_keys("passed")

            email_input.send_keys(email)
            username_input.send_keys(username)
            password_input.send_keys(password)
            self.browser.find_element(By.ID, "submit_button").click()

    def create_post(self, header='header test', body= 'body test'):

        self.browser.get(f'{self.live_server_url}{reverse('posts:post_form')}')
        self.browser.find_element(By.ID, 'post_form')
        header_input = self.browser.find_element(By.NAME, 'header_input')
        body_input = self.browser.find_element(By.NAME, 'body_input')

        header_input.send_keys(header)
        body_input.send_keys(body)
        self.browser.find_element(By.ID, 'submit').click()

    def test_can_see_the_homepage(self):
        self.browser.get(self.live_server_url)

        # Farshad immediately notices the page title mentioning 'Deep Talk'
        self.assertIn('Talk' , self.browser.title)
    
        # he can see a button on top of the page which reads as "+ Create Post"
        button = self.browser.find_element(By.ID, 'create_post_button')

        self.assertEqual('+ create post', button.text.lower())
        button.click()

         # Farshad sees a sign-un form instead, he understand that he needs to sign-up first using email
        # he does so

        self.assertEqual(urlparse(self.browser.current_url).path, reverse('sign_up'))

        self.assertIn('email:', self.browser.page_source.lower())
        self.assertIn('username:', self.browser.page_source.lower())
        self.assertIn('password:', self.browser.page_source.lower())

        self.sign_up()

        # after signing-in, he is redirected to the homepage
        self.assertEqual(urlparse(self.browser.current_url).path, reverse('home'))
        self.browser.find_element(By.ID, 'create_post_button').click()

        # he sees a form where he can type in a heading and the body of the post

        self.browser.find_element(By.ID, 'post_form')
        header = self.browser.find_element(By.NAME, 'header_input')
        body = self.browser.find_element(By.NAME, 'body_input')

        self.assertEqual(header.get_attribute('placeholder'), 'Enter the heading')
        self.assertEqual(body.get_attribute('placeholder'), 'Enter the body')

        # Farshad wants to write a post about extreme climate and its effects on puppies 
        header.send_keys('extreme climate and its effects on puppies')

        body.send_keys('Extreme climate, whether scorching heat or freezing cold, can severely affect puppies.' \
        'High temperatures can cause dehydration and heatstroke, while extreme cold can lead to hypothermia'
        ' and frostbite. Puppies are especially vulnerable because their bodies cannot regulate temperature' \
        ' well. Proper shelter, hydration, and care are essential to keep them safe in harsh weather.')

        # after creating the post, he clicks the submit button and it redirects him where he can see his post 
        self.browser.find_element(By.ID, 'submit').click()
        posted_header= self.browser.find_element(By.ID, 'posted_header').text
        posted_body = self.browser.find_element(By.ID, 'posted_body').text

        self.assertEqual(posted_header, "extreme climate and its effects on puppies")
        self.assertIn("Puppies are especially vulnerable because their bodies cannot regulate temperature",
                       posted_body)
        # after checking his post, Farshad wants to go back to the home page
        # so he clicks on the name of the website visible on the top-left of the page which redirects him-
        # to the hamepage 

        self.browser.find_element(By.ID, 'home_redirect').click()
        url = self.browser.current_url
        self.assertEqual(urlparse(url).path, reverse('home'))

        # he creates another post and returns to the home page when he's done
        self.create_post(header='Why puppies are the best!',
                        body='Becasue they woof-woof all the time!')
        
        self.browser.find_element(By.ID, 'home_redirect').click()

        # Farshad suddenly remembers that he hadn't checked if he has written all the
        # reasons for why the puppies are the best
        # so he uses the navigation feature at the right corner of the home page called 'My Posts'
        # after clicking on it, he can see a page displaying the headers of his 2 posts

        my_posts_clickable= self.browser.find_element(By.ID, 'my_posts')
        self.assertEqual(my_posts_clickable.text, 'My Posts')

        my_posts_clickable.click()

        assert self.browser.find_elements(By.TAG_NAME, 'p'), "<p> element not found"

        headers = ['Why puppies are the best!',"extreme climate and its effects on puppies"]
        posts = self.browser.find_elements(By.CLASS_NAME, 'my_posts')
        for post in posts:
            self.assertIn(post.text, headers)

        # he clicks on his first post and navigates to see the details of the post 
        post_link = posts[0].find_element(By.TAG_NAME, 'a')
        post_link.click()

        # in the post page he can delete or edit the post using delete and edit buttons 
        delete_button= self.browser.find_element(By.ID, 'delete_post')
        self.browser.find_element(By.ID, 'edit_post')

        # and he decised to delete the post
        delete_button.click()
        self.assertEqual(urlparse(self.browser.current_url).path, reverse('posts:post_manager'))

        posts = self.browser.find_elements(By.CLASS_NAME, 'my_posts')
        for post in posts:
            self.assertNotEqual('Why puppies are the best!', post.text)

        # he then decides to add some more text to his first post in order to explain the hazards of the extreame 
        # wheather more thoroughly; he navigates to the post page and clicks edit button:

        post_link= posts[0].find_element(By.TAG_NAME, 'a')
        post_link.click()

        edit_button= self.browser.find_element(By.ID, 'edit_post')
        edit_button.click()

        # he can see the exact form he used to write this post but this time the inputs are pre-filled with 
        # what he wrote before

        body = self.browser.find_element(By.NAME, 'body_input')
        body.send_keys('During hot weather, ensure they have access to shade and fresh water at all times.')

        self.browser.find_element(By.ID, 'submit').click()
        time.sleep(5)
        posted_header= self.browser.find_element(By.ID, 'posted_header').text
        posted_body = self.browser.find_element(By.ID, 'posted_body').text

        self.assertEqual(posted_header, "extreme climate and its effects on puppies")
        self.assertIn(
            (
                "Extreme climate, whether scorching heat or freezing cold, can severely affect puppies."
                "High temperatures can cause dehydration and heatstroke, while extreme cold can lead to hypothermia "
                "and frostbite. Puppies are especially vulnerable because their bodies cannot regulate temperature well. "
                "Proper shelter, hydration, and care are essential to keep them safe in harsh weather."
                "During hot weather, ensure they have access to shade and fresh water at all times."
            ),
            posted_body
        )


        # satisfied by the result, he closes the browser, excited to see if anyone actually reads him or not 

    def test_multiple_users_can_use_the_site_without_interfering_each_other(self):

        #Farshad logs-in again and creates a post
        self.sign_up(username='Farshad')
        self.create_post(header='Why puppies are the best!',
                          body='Becasue they woof-woof all the time!')
        time.sleep(0.1) 
        
        # he's not really in the mood to write more than he already did, so he just gazes into the screen 
        #in the meantime a new user, Sara wants to try this awsome site!
        self.browser.delete_all_cookies() ## to switch users
        user =User.objects.create_user(username='Sara', email='sara@gmail.com', password='sara')
        post_obj= Post.objects.create(user= user,header='Why kitties are the best!',body='Cause they wanna watch the world burn :3')
          
        # She goes to check her post in the My Posts section where she can only see her posts...
        self.login(email='sara@gmail.com', password='sara')
        self.browser.get(f'{self.live_server_url}{reverse('posts:post_manager')}')
        posts = self.browser.find_elements(By.CLASS_NAME, 'my_posts' )
        my_posts = [post.text for post in posts]
        self.assertNotIn('Why puppies are the best!', my_posts)
        self.assertIn('Why kitties are the best!', my_posts)

        # While Sara is checking her post, Farshad is keep refereshing the homepage to see if anyone
        # has posted anything. it's lonesome to be the only user of the website after all
        # and suddenly BANG! Farshad sees his post and another user's post with the username "Sara"!
 
        self.browser.delete_all_cookies()
        self.login() ## this must redirect to the homepage by default
        
        # the posts are ordered based on the publish date and time. newer to older
        # Farshad can see the author username on the post

        feed_post= self.browser.find_elements(By.CLASS_NAME, 'feed_post')

        post_header = self.browser.find_elements(By.CLASS_NAME, 'post_header')
        post_author = self.browser.find_elements(By.CLASS_NAME, 'post_author')

        headers = ['Why kitties are the best!', 'Why puppies are the best!']
        authors = ['Sara', 'Farshad']
        for i in range(0, len(feed_post)):
            self.assertEqual(headers[i],post_header[i].text)
            self.assertEqual(authors[i], post_author[i].text)

        # he clicks the post and navigates to see the full version of the post
        post_header[0].find_element(By.TAG_NAME, 'a').click()
        self.assertEqual(urlparse(self.browser.current_url).path, reverse('posts:post_view', args=[post_obj.id]))

    def test_user_can_navigate_through_paginated_posts(self):
        """Users can browse multiple pages of posts"""
        # Create many posts
        user = User.objects.create_user(
            username='prolific_writer',
            email='writer@gmail.com',
            password='pass'
        )
        for i in range(25):
            Post.objects.create(
                user=user,
                header=f'Post {i}',
                body=f'Body {i}'
            )
        
        self.browser.get(self.live_server_url)
        
        # Should see pagination
        pagination = self.browser.find_element(By.CLASS_NAME, 'pagination')
        self.assertTrue(pagination.is_displayed())
        
        # Get first post header on page 1
        first_post = self.browser.find_element(By.CLASS_NAME, 'post_header').text
        
        # Navigate to page 2
        page2_link = self.browser.find_element(By.LINK_TEXT, '2')
        page2_link.click()
        
        # Should be on page 2 now
        self.assertIn('page=2', self.browser.current_url)
        
        # Should see different posts
        first_post_page2 = self.browser.find_element(By.CLASS_NAME, 'post_header').text
        self.assertNotEqual(first_post, first_post_page2)

class UsersDontSeeInternalErrorsTest(NewVisitorTest):

    # Farshid, Farshad's older brother heard about a cool site where he can create a post for others to read
    # and wants to try it himself, he tries signing up; but because of him being a clumpsy silly goose
    # he fais the first attempt because of a typo! He enters Farshad instead of Farshid in the email address!

    def test_users_must_complete_a_captcha_when_signing_up(self):
        self.sign_up()
        url = self.browser.current_url
        self.assertEqual(urlparse(url).path, reverse('home'))
    
    def test_users_are_informed_that_the_email_theyre_using_has_been_used_before_when_signing_up(self):
        ## this is Farshad's account!
        self.sign_up(email='Farshad@gmail.com', username='Farshad', password='1234')
        self.browser.delete_all_cookies()
        ## Farshid tries to sign up
        self.sign_up(email='Farshad@gmail.com', username='Farshad', password='41148')
        #He sees an error message in the sign_up page saying a user with this email and username already exsits
        self.assertIn('a user with this email already exists!',self.browser.page_source.lower())
        self.assertIn('this username is taken!', self.browser.page_source.lower())

        # he tries again; but this time he doesn't use the correct username
        self.sign_up(email='Farshid@gmail.com', username='Farshad', password='41148')
        self.assertNotIn('a user with this email already exists!', self.browser.page_source.lower())

        # and again; this time with an incorrect email but a correct username
        self.sign_up(email='Farshad@gmail.com', username='Farshid', password='41148')
        self.assertNotIn('this username is taken!', self.browser.page_source.lower())