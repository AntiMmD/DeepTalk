from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from django.test import LiveServerTestCase
from django.urls import reverse
from urllib.parse import urlparse

        # Farshad has recently heard about a cool website where he can write a blog post and share it with others
        # he opens his browser and checks the homepage 

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

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
        self.browser.get(f'{self.live_server_url}{reverse('sign_up')}')
        email_input= self.browser.find_element(By.ID, "email_input")
        username_input= self.browser.find_element(By.ID, "username_input")
        password_input= self.browser.find_element(By.ID, "password_input")
                
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
        self.browser.find_element(By.TAG_NAME, 'button').click()


    def test_can_see_the_homepage(self):
        self.browser.get(self.live_server_url)

        # Farshad immediately notices the page title and header mentioning 'Monologue'
        header_text = self.browser.find_element( By.TAG_NAME, 'h1' ).text
        self.assertIn('Welcome to Monologue!' , self.browser.title)
        self.assertEqual('Monologue!' , header_text)
        
        # he can see a button under the header which reads as "create a post"
        button = self.browser.find_element(By.ID, 'create_post_button')

        self.assertEqual('create a post', button.text.lower())
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
        self.browser.find_element(By.TAG_NAME, 'button').click()
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
        
        # self.fail('finish the test')

        # satisfied by the result, he closes the browser, excited to see if anyone actually reads him or not 

    def test_multiple_users_can_use_the_site_without_interfering_each_other(self):

        #Farshad logs-in again and creates a post
        self.sign_up()
        self.browser.delete_all_cookies() ## to simulate a new user
        self.login()

        self.create_post(header='Why puppies are the best!',
                          body='Becasue they woof-woof all the time!')
        
        # in the meantime, a new user, Sara is doing the same thing!

        self.sign_up(email='sara@gmail.com', username='sara', password='sara')
        self.browser.delete_all_cookies()
        self.login(email='sara@gmail.com', password='sara') 
        self.create_post(header='Why kitties are the best!', body='Cause they wanna watch the world burn :3')
        
        # She goes to check her post in the My Posts section where she can only see her posts

        self.browser.get(f'{self.live_server_url}{reverse('posts:post_manager')}')
        posts = self.browser.find_elements(By.CLASS_NAME, 'my_posts' )
        my_posts = [post.text for post in posts]
        self.assertNotIn('Why puppies are the best!', my_posts)
        self.assertIn('Why kitties are the best!', my_posts)

class UsersDontSeeInternalErrors(NewVisitorTest):

    # Farshid, Farshad's older brother heard about a cool site where he can create a post for others to read
    # and wants to try it himself, he tries signing up; but because of him being a clumpsy silly goose
    # he fais the first attempt because of a typo! He enters Farshad instead of Farshid in the email address!
    
    def test_users_are_informed_that_the_email_theyre_using_has_been_used_before_when_signing_up(self):
        ## this is Farshad's account!
        self.sign_up(email='Farshad@gmail.com', username='Farshad', password='1234')
        self.browser.delete_all_cookies()
        ## Farshid tries to sign up
        self.sign_up(email='Farshad@gmail.com', username='Farshad', password='41148')
        #He sees an error message in the sign_up page saying a user with this email already exsits

        email_error = self.browser.find_element(By.ID, 'email_error').text
        self.assertEqual('a user with this email address exists!', email_error.lower())