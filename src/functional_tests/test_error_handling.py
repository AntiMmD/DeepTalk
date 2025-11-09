from django.urls import reverse
from urllib.parse import urlparse
from django.contrib.auth import get_user_model
from .base import FunctionalTest
User = get_user_model()

class UsersDontSeeInternalErrorsTest(FunctionalTest):

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